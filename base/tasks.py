from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests
import psutil
import json

from .models import Service, MetricLog, PipelineRun, Alert, System
from .utils import sendtelegrammsg, send_alert

@shared_task
def check_system_status():
    for system in System.objects.all():

        if system.status == 'up' and (system.last_check == None or system.last_check < timezone.now() - timedelta(minutes=5)):
            system.last_status_change = timezone.now()
            system.status = 'down'
            system.save()
            sendtelegrammsg(f'{system.name} is down')

        if system.status == 'down':
            if system.last_status_change < timezone.now() - timedelta(days=1):
                sendtelegrammsg(f'{system.name} is down for more than 1 day')
            
            elif system.last_status_change < timezone.now() - timedelta(hours=12):
                sendtelegrammsg(f'{system.name} is down for more than 12 hours')
            
            elif system.last_status_change < timezone.now() - timedelta(hours=6):
                sendtelegrammsg(f'{system.name} is down for more than 6 hours')

            elif system.last_status_change < timezone.now() - timedelta(hour = 1):
                sendtelegrammsg(f'{system.name} is down for more than 1 hour')

@shared_task
def check_service_health():
    """Check health of all registered services"""
    for service in Service.objects.all():
        try:
            # Make health check request
            response = requests.get(service.endpoint, timeout=5)
            new_status = 'up' if response.status_code == 200 else 'down'
            
            # Record response time
            MetricLog.objects.create(
                service=service,
                metric_type='response_time',
                value=response.elapsed.total_seconds()
            )
            
        except requests.RequestException:
            new_status = 'down'
        
        # Handle status changes
        if service.status != new_status:
            service.status = new_status
            service.last_status_change = timezone.now()
            
            # Create alert for status change
            Alert.objects.create(
                service=service,
                title=f'{service.get_name_display()} Status Change',
                message=f'Service status changed to {new_status}',
                severity=4 if new_status == 'down' else 2
            )
        
        service.last_check = timezone.now()
        service.save()

@shared_task
def collect_system_metrics():
    """Collect system metrics for all services"""
    for service in Service.objects.all():
        # Example metrics collection - customize based on your needs
        if service.status == 'up':
            # CPU Usage
            MetricLog.objects.create(
                service=service,
                metric_type='cpu_usage',
                value=psutil.cpu_percent()
            )
            
            # Memory Usage
            memory = psutil.virtual_memory()
            MetricLog.objects.create(
                service=service,
                metric_type='memory_usage',
                value=memory.percent
            )
            
            # Disk Usage
            disk = psutil.disk_usage('/')
            MetricLog.objects.create(
                service=service,
                metric_type='disk_usage',
                value=disk.percent
            )

@shared_task
def check_pipeline_status():
    """Monitor pipeline runs and alert on failures"""
    # Check for long-running pipelines
    running_pipelines = PipelineRun.objects.filter(
        status='running',
        start_time__lt=timezone.now() - timedelta(hours=1)
    )
    
    for pipeline in running_pipelines:
        Alert.objects.create(
            pipeline_run=pipeline,
            title=f'Long Running Pipeline: {pipeline.get_pipeline_type_display()}',
            message=f'Pipeline has been running for over 1 hour',
            severity=2
        )
    
    # Check for failed pipelines
    failed_pipelines = PipelineRun.objects.filter(
        status='failed',
        timestamp__gte=timezone.now() - timedelta(minutes=5)
    )
    
    for pipeline in failed_pipelines:
        Alert.objects.create(
            pipeline_run=pipeline,
            title=f'Pipeline Failure: {pipeline.get_pipeline_type_display()}',
            message=f'Pipeline failed: {pipeline.error_message}',
            severity=3
        )

@shared_task
def cleanup_old_metrics():
    """Clean up old metric logs to prevent database bloat"""
    # Keep last 30 days of metrics
    cutoff_date = timezone.now() - timedelta(days=30)
    MetricLog.objects.filter(timestamp__lt=cutoff_date).delete()