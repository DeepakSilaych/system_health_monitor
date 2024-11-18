from rest_framework import serializers
from .models import Service, MetricLog, PipelineRun, Alert

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'status', 'last_check', 'last_status_change', 'endpoint']

class MetricLogSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = MetricLog
        fields = ['id', 'service', 'service_name', 'metric_type', 'value', 'timestamp']

class PipelineRunSerializer(serializers.ModelSerializer):
    pipeline_type_display = serializers.CharField(source='get_pipeline_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PipelineRun
        fields = ['id', 'pipeline_type', 'pipeline_type_display', 'status', 
                 'status_display', 'start_time', 'end_time', 'error_message', 'metadata']

class AlertSerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    pipeline_type = serializers.CharField(source='pipeline_run.pipeline_type', read_only=True)
    
    class Meta:
        model = Alert
        fields = ['id', 'service', 'service_name', 'pipeline_run', 'pipeline_type',
                 'title', 'message', 'severity', 'severity_display', 'timestamp',
                 'acknowledged', 'acknowledged_by', 'acknowledged_at']
