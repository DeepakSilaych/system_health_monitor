from django.utils import timezone
from django.conf import settings
import requests

def send_alert(title, message, severity=1):
    """
    Send an alert through configured notification channels.
    Severity levels:
    1 - Info
    2 - Warning
    3 - Critical
    """
    from .models import Alert
    
    alert = Alert.objects.create(
        title=title,
        message=message,
        severity=severity,
        timestamp=timezone.now()
    )
    
    # Send to external notification services if configured
    if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and hasattr(settings, 'TELEGRAM_CHAT_ID'):
        try:
            requests.post(
                f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
                json={
                    'chat_id': settings.TELEGRAM_CHAT_ID,
                    'text': f'[{alert.get_severity_display()}] {title}\n\n{message}'
                }
            )
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")
    
    return alert
