from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Log, Backend, Automation
from .serializers import LogSerializer, BackendSerializer, AutomationSerializer
from django.utils import timezone
import requests
from django.shortcuts import render

class LogViewSet(APIView):
    def post(self, request):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        logs = Log.objects.all().order_by('-log_date')
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)

class BackendViewSet(APIView):
    def get(self, request):
        backends = Backend.objects.all()
        serializer = BackendSerializer(backends, many=True)
        return Response(serializer.data)

    def check_backend_health(self):
        backends = Backend.objects.all()
        for backend in backends:
            try:
                response = requests.get(f'http://{backend.url}/health/')
                if response.status_code == 200 and response.json().get('status') == 'up':
                    backend.status = 'up'   
                else:
                    backend.status = 'down'
            except requests.RequestException:
                backend.status = 'down'
            finally:
                backend.last_check = timezone.now()
                if backend.status == 'up':
                    backend.last_status_change_to_up = timezone.now()
                backend.save()

class AutomationViewSet(APIView):
    def get(self, request):
        automations = Automation.objects.all()
        serializer = AutomationSerializer(automations, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'index.html')