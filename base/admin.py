from django.contrib import admin
from .models import Service, MetricLog, PipelineRun, Alert

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'last_check', 'last_status_change')
    list_filter = ('status',)
    search_fields = ('name',)

@admin.register(MetricLog)
class MetricLogAdmin(admin.ModelAdmin):
    list_display = ('service', 'metric_type', 'value', 'timestamp')
    list_filter = ('service', 'metric_type')
    date_hierarchy = 'timestamp'

@admin.register(PipelineRun)
class PipelineRunAdmin(admin.ModelAdmin):
    list_display = ('pipeline_type', 'status', 'start_time', 'end_time')
    list_filter = ('pipeline_type', 'status')
    search_fields = ('error_message',)
    date_hierarchy = 'start_time'

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'timestamp', 'acknowledged')
    list_filter = ('severity', 'acknowledged')
    search_fields = ('title', 'message')
    date_hierarchy = 'timestamp'