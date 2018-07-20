# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    path('api-key/', views.ApiKeyDetailView.as_view(), name='api-key'),
    path('users/', include('users.urls'), name='users'),
    path('document_manager/', include('document_manager.urls'), name='document_manager')
]