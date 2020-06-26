# -*- coding: utf-8 -*-
from django.urls import path

from .views import (
    CompanyUpdate,
    FacebookAuth,
    GoogleAuth,
    SectorList,
    UserChangeEmail,
    UserChangePassword,
    UserDetail,
    UserNameUpdate,
    UserProfessionUpdate
)

app_name = 'users'

urlpatterns = [
    path('auth/facebook/', FacebookAuth.as_view(), name='fb_login'),
    path('auth/google/', GoogleAuth.as_view(), name='gl_login'),
    path('auth/user/', UserDetail.as_view(), name='user-detail'),
    path('profile/<int:pk>/', UserNameUpdate.as_view(), name='user_name_update'),
    path('profile/profession/', UserProfessionUpdate.as_view(), name='user_profession_update'),
    path('change-email/', UserChangeEmail.as_view(), name='user_change_email'),
    path('change-password/', UserChangePassword.as_view(), name='user_change_password'),
    path('sectors/', SectorList.as_view(), name='sector_list'),
    path('company-update/', CompanyUpdate.as_view(), name='company_update'),
]
