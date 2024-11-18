from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
import json
import traceback
import requests

from .models import Service, MetricLog, PipelineRun, Alert
from .serializers import ServiceSerializer, MetricLogSerializer, PipelineRunSerializer, AlertSerializer
from .utils import send_alert

def send_telegram_error(error_msg):
    """Send error message to Telegram"""
    base = 'https://api.telegram.org/bot7334081801:AAFYpGcHtxyqllOYYigyyO2EHGYBGPIN6ss/'
    chatid = '-4238563016'
    url = base + 'sendMessage'
    try:
        requests.post(url, json={
            'chat_id': chatid,
            'text': f' Error in System Monitor:\n{error_msg}'
        })
    except Exception as e:
        print(f"Failed to send error to Telegram: {e}")

def dashboard(request):
    """Main monitoring dashboard view"""
    try:
        context = {
            'services': Service.objects.all(),
            'recent_alerts': Alert.objects.filter(
                acknowledged=False
            ).order_by('-severity', '-timestamp')[:10],
            'active_pipelines': PipelineRun.objects.filter(
                status__in=['running', 'pending']
            ).order_by('-start_time')
        }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        error_msg = f"Dashboard Error: {str(e)}\n{traceback.format_exc()}"
        send_telegram_error(error_msg)
        raise

class ServiceStatusView(APIView):
    """Handle service status updates and queries"""
    def get(self, request):
        try:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_msg = f"Service Status Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise
    
    def post(self, request):
        try:
            service = Service.objects.get(name=request.data.get('name'))
            service.status = request.data.get('status', 'unknown')
            service.last_check = timezone.now()
            
            if service.status != request.data.get('status'):
                service.last_status_change = timezone.now()
            
            service.save()
            return Response({'status': 'updated'})
        except Exception as e:
            error_msg = f"Service Update Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise

class MetricsView(APIView):
    """Handle metrics data"""
    def get(self, request):
        try:
            service_name = request.query_params.get('service')
            metric_type = request.query_params.get('metric_type')
            hours = int(request.query_params.get('hours', 24))
            
            metrics = MetricLog.objects.filter(
                timestamp__gte=timezone.now() - timedelta(hours=hours)
            )
            
            if service_name:
                metrics = metrics.filter(service__name=service_name)
            if metric_type:
                metrics = metrics.filter(metric_type=metric_type)
                
            serializer = MetricLogSerializer(metrics, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_msg = f"Metrics Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise
    
    def post(self, request):
        try:
            service = Service.objects.get(name=request.data.get('service'))
            MetricLog.objects.create(
                service=service,
                metric_type=request.data.get('metric_type'),
                value=request.data.get('value')
            )
            return Response({'status': 'created'})
        except Exception as e:
            error_msg = f"Metrics Creation Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise

class PipelineStatusView(APIView):
    """Handle pipeline status updates"""
    def get(self, request):
        try:
            pipeline_type = request.query_params.get('type')
            status = request.query_params.get('status')
            
            pipelines = PipelineRun.objects.all()
            if pipeline_type:
                pipelines = pipelines.filter(pipeline_type=pipeline_type)
            if status:
                pipelines = pipelines.filter(status=status)
                
            serializer = PipelineRunSerializer(pipelines, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_msg = f"Pipeline Status Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise
    
    def post(self, request):
        try:
            pipeline = PipelineRun.objects.create(
                pipeline_type=request.data.get('pipeline_type'),
                status=request.data.get('status', 'running'),
                metadata=request.data.get('metadata', {})
            )
            
            if request.data.get('status') == 'failed':
                pipeline.error_message = request.data.get('error_message')
                pipeline.save()
                
                Alert.objects.create(
                    pipeline_run=pipeline,
                    title=f'Pipeline Failure: {pipeline.get_pipeline_type_display()}',
                    message=pipeline.error_message,
                    severity=3
                )
            
            return Response({'id': pipeline.id})
        except Exception as e:
            error_msg = f"Pipeline Creation Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise

class AlertView(APIView):
    """Handle system alerts"""
    def get(self, request):
        try:
            acknowledged = request.query_params.get('acknowledged')
            severity = request.query_params.get('severity')
            
            alerts = Alert.objects.all()
            if acknowledged is not None:
                alerts = alerts.filter(acknowledged=acknowledged)
            if severity:
                alerts = alerts.filter(severity=severity)
                
            serializer = AlertSerializer(alerts, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_msg = f"Alert Query Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise
    
    def post(self, request):
        """Acknowledge an alert"""
        try:
            alert = Alert.objects.get(id=request.data.get('alert_id'))
            alert.acknowledged = True
            alert.acknowledged_by = request.data.get('user')
            alert.acknowledged_at = timezone.now()
            alert.save()
            return Response({'status': 'acknowledged'})
        except Exception as e:
            error_msg = f"Alert Acknowledgment Error: {str(e)}\n{traceback.format_exc()}"
            send_telegram_error(error_msg)
            raise