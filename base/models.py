from django.db import models

class Log(models.Model):
    log_text = models.CharField(max_length=200)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True)

    def __str__(self):
        return self.log_text
    
class Backend(models.Model):
    status = models.CharField(choices=[('up', 'Up'), ('down', 'Down')], max_length=4)
    last_check = models.DateTimeField('last checked', auto_now_add=True)
    last_status_change = models.DateTimeField('last status change')
    last_status_change_to_up = models.DateTimeField('last status change to up')

    def __str__(self):
        return self.status

class Automation(models.Model):
    automation_name = models.CharField(max_length=200)
    automation_description = models.CharField(max_length=200)
    automation_status = models.CharField(choices=[('ongoing', 'Ongoing'), ('stopped', 'Stopped')], max_length=7)
    automation_last_run = models.DateTimeField('last run')
    automation_next_run = models.DateTimeField('next run')

    def __str__(self):
        return self.automation_name
    