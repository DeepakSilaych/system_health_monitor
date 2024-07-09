from django.db import models


class Log(models.Model):
    log_text = models.CharField(max_length=200)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.log_text

    def get_priority_class(self):
        if self.priority == 0:
            return 'low-priority'
        elif self.priority == 1:
            return 'medium-priority'
        elif self.priority == 2:
            return 'high-priority'
        else:
            return 'default-priority'

    
class System(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    status = models.CharField(choices=[('up', 'Up'), ('down', 'Down')], max_length=4)
    last_check = models.DateTimeField('last check')
    last_status_change = models.DateTimeField('last status change')

    def __str__(self):
        return self.name
