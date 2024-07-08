from django.contrib import admin
from django.urls import path
from base.views import LogViewSet, BackendViewSet, AutomationViewSet, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('logs/', LogViewSet.as_view(), name='logs'),
    path('backends/', BackendViewSet.as_view(), name='backends'),
    path('automations/', AutomationViewSet.as_view(), name='automations'),
]
