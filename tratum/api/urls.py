# -*- coding: utf-8 -*-
from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [
    path('api-key/', views.ApiKeyDetailView.as_view(), name='api-key'),
    path('users/', include('tratum.users.urls'), name='users'),
    path('document-manager/', include('tratum.document_manager.urls'), name='document_manager'),
    path('store/', include('tratum.store.urls'), name='store')
]
