from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Service, MetricLog, PipelineRun, Alert
import random

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create services
        services = [
            Service.objects.create(name='Data Pipeline', status='up', endpoint='http://data-pipeline:8000'),
            Service.objects.create(name='ML Service', status='up', endpoint='http://ml-service:8000'),
            Service.objects.create(name='API Gateway', status='up', endpoint='http://api-gateway:8000'),
            Service.objects.create(name='Database', status='up', endpoint='http://database:5432'),
        ]
        self.stdout.write('Created services')

        # Create metrics
        for service in services:
            for _ in range(5):
                MetricLog.objects.create(
                    service=service,
                    metric_type=random.choice(['cpu', 'memory', 'disk', 'network']),
                    value=random.uniform(0, 100)
                )
        self.stdout.write('Created metrics')

        # Create pipeline runs
        pipeline_types = ['data_ingestion', 'preprocessing', 'training', 'evaluation']
        statuses = ['running', 'completed', 'failed']
        
        for _ in range(5):
            PipelineRun.objects.create(
                pipeline_type=random.choice(pipeline_types),
                status=random.choice(statuses),
                start_time=timezone.now(),
                end_time=timezone.now() if random.choice([True, False]) else None,
                error_message='Sample error' if random.choice([True, False]) else None
            )
        self.stdout.write('Created pipeline runs')

        # Create alerts
        severities = [1, 2, 3]  # Info, Warning, Critical
        for service in services:
            Alert.objects.create(
                service=service,
                title=f'Test Alert for {service.name}',
                message=f'This is a test alert for {service.name}',
                severity=random.choice(severities)
            )
        self.stdout.write('Created alerts')
