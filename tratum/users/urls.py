# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^auth/facebook/$', views.FacebookAuth.as_view(), name='fb_login'),
    url(r'^auth/google/$', views.GoogleAuth.as_view(), name='gl_login'),
    url(r'^auth/user/$', views.UserDetail.as_view(), name='user-detail'),
    path('profile/<int:pk>/', views.UserNameUpdate.as_view(), name='user_name_update'),
    path('change-email/', views.UserChangeEmail.as_view(), name='user_change_email'),
    path('change-password/', views.UserChangePassword.as_view(), name='user_change_password'),
    path('sectors/', views.SectorList.as_view(), name='sector_list'),
    path('company-update/', views.CompanyUpdate.as_view(), name='company_update'),
]
