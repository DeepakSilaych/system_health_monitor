from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Log, System
from .serializers import LogSerializer
from django.utils import timezone
from django.shortcuts import render

from django.utils import timezone
from datetime import timedelta

from .utils import sendtelegrammsg

class LogViewSet(APIView):
    def post(self, request):
        data = {
            'log_text': request.data.get('log_text'),
            'priority': request.data.get('priority') if request.data.get('priority') else 0
        }

        if data['priority'] > 0:
            try :
                sendtelegrammsg(data['log_text'])
            except:
                pass

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

        if system.status == 'down':
            sendtelegrammsg(f'{system.name} is up')
            system.status = 'up'
            system.last_status_change = timezone.now()

        system.last_check = timezone.now()     
        system.save()

        return Response({'status': system.status})


def index(request):
    logs = Log.objects.all().order_by('-timestamp')[:10000]
    systems = System.objects.all()

    context = {
        'logs': logs,
        'systems': systems,
    }

    return render(request, 'index.html', context)