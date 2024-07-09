from django.contrib import admin
from django.urls import path
from base.views import LogViewSet, index , Systemlog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('logs/', LogViewSet.as_view(), name='logs'),
    path('systemlog/', Systemlog.as_view(), name='systemlog'),
]
