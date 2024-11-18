from django.contrib import admin
from django.urls import path
from base.views import (
    dashboard,
    ServiceStatusView,
    MetricsView,
    PipelineStatusView,
    AlertView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('services/', ServiceStatusView.as_view(), name='services'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
    path('pipelines/', PipelineStatusView.as_view(), name='pipelines'),
    path('alerts/', AlertView.as_view(), name='alerts'),
]
