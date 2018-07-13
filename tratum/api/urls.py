# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

app_name = 'api'
urlpatterns = [
    url(r'^api-key/', views.ApiKeyDetailView.as_view(), name='api-key'),
    url(r'^users/', include('users.urls')),
]