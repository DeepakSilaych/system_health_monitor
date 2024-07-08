from .models import Log, Backend, Automation
from rest_framework import serializers

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['log_text', 'log_date']

class BackendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backend
        fields = ['status', 'last_check', 'last_status_change', 'last_status_change_to_up']

class AutomationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Automation
        fields = ['automation_name', 'automation_description', 'automation_status', 'automation_last_run', 'automation_next_run']