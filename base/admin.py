from django.contrib import admin
from .models import Log, Backend, Automation
# Register your models here.

admin.site.register(Log)
admin.site.register(Backend)
admin.site.register(Automation)