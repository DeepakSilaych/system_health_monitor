from .models import Log, System
from rest_framework import serializers

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields =  '__all__'

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'
