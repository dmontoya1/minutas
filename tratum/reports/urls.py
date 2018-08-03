from django.conf.urls import url
from django.urls import path, include
from .views import DocumentExport

app_name = 'reports'

urlpatterns = [
    path('document-sales/', DocumentExport.as_view(), name='document-sales'),
]