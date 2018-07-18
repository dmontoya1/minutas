# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^auth/facebook/$', views.FacebookAuth.as_view(), name='fb_login'),
    url(r'^auth/google/$', views.GoogleAuth.as_view(), name='gl_login'),
    url(r'^auth/user/$', views.UserDetail.as_view(), name='user-detail'),
]
