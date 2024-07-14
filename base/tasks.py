from celery import shared_task
from django.conf import settings
from .utils import sendtelegrammsg
from models import System
from datetime import timedelta
from django.utils import timezone

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

            


        