from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Log, System
from .serializers import LogSerializer
from django.utils import timezone
from django.shortcuts import render

from django.utils import timezone
from datetime import timedelta

class LogViewSet(APIView):
    def post(self, request):
        data = {
            'log_text': request.data.get('log_text'),
            'priority': request.data.get('priority') if request.data.get('priority') else 0
        }

        Log.objects.create(log_text=data['log_text'], priority=data['priority'])
        return Response({'status': 'Log created'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        logs = Log.objects.all().order_by('-timestamp')
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

class Systemlog(APIView):
    def post(self, request):
        data = {
            'code': request.data.get('code'),
        }
        system = System.objects.get(name=data['code'])
        system.status = 'up'

        system.last_check = timezone.now()     
        system.save()

        return Response({'status': system.status})


def index(request):
    logs = Log.objects.all().order_by('-timestamp')
    systems = System.objects.all()

    for system in systems:
        if system.last_check == None or system.last_check < timezone.now() - timedelta(minutes=5):
            system.status = 'down'
        system.save()

    context = {
        'logs': logs,
        'systems': systems,
    }

    return render(request, 'index.html', context)