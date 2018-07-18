# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

from rest_framework import generics
from rest_framework.response import Response

from api.helpers import get_api_user
from .serializers import UserSerializer
from .models import User, LogTerms


class FacebookAuth(SocialLoginView):
    """Facebook Authentication
    """
    adapter_class = FacebookOAuth2Adapter


class GoogleAuth(SocialLoginView):
    """Google Authentication
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def __init__(self):
        self.callback_url = self.get_callback_url()

    def get_callback_url(self):
        domain = Site.objects.get_current().domain
        return 'https://{domain}/api/accounts/google/login/callback/'.format(domain=domain)


class UserDetail(generics.RetrieveUpdateAPIView):
    """Api para obtener y actualizar el campo de aceptó términos y condiciones
    para un usuario que se registró en la plataforma
    """

    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        user = get_api_user(self.request)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        log = LogTerms(
            ip=ip,
            user=user
        )
        log.save()
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return get_api_user(self.request)

    def get_queryset(self):
        return get_user_model().objects.none()
    