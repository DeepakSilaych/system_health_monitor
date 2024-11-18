from django.db import models
from django.utils import timezone

class Service(models.Model):
    """Represents a monitored service (Frontend, Backend, ML Pipeline, Data Fetcher)"""
    NAME_CHOICES = [
        ('frontend', 'Frontend Service'),
        ('backend', 'Backend Service'),
        ('ml_pipeline', 'ML Pipeline'),
        ('data_fetcher', 'Data Fetcher')
    ]
    
    name = models.CharField(max_length=50, choices=NAME_CHOICES, unique=True)
    status = models.CharField(max_length=20, default='unknown')
    last_check = models.DateTimeField(null=True)
    last_status_change = models.DateTimeField(null=True)
    endpoint = models.URLField(max_length=200)
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.status}"

class MetricLog(models.Model):
    """Stores service metrics like CPU, memory usage, response times"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=50)  # cpu, memory, response_time, etc.
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        indexes = [
            models.Index(fields=['service', 'metric_type', 'timestamp'])
        ]

class PipelineRun(models.Model):
    """Tracks ML and data pipeline runs"""
    PIPELINE_CHOICES = [
        ('data_fetch', 'Data Fetching'),
        ('data_process', 'Data Processing'),
        ('model_train', 'Model Training'),
        ('prediction', 'Prediction Generation')
    ]
    
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ]
    
    pipeline_type = models.CharField(max_length=50, choices=PIPELINE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True)
    error_message = models.TextField(null=True, blank=True)
    metadata = models.JSONField(default=dict)  # Store additional pipeline-specific data
    
    class Meta:
        indexes = [
            models.Index(fields=['pipeline_type', 'status', 'start_time'])
        ]

class Alert(models.Model):
    """System alerts and notifications"""
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    pipeline_run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.CharField(max_length=100, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['severity', 'timestamp', 'acknowledged'])
        ]
