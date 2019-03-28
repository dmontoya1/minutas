# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from tratum.api.helpers import get_api_user

from .serializers import UserSerializer, ChangePasswordSerializer, SectorSerializer, CompanySerializer
from .models import User, LogTerms, Sector, Company


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


class UserNameUpdate(generics.UpdateAPIView):
    """ Api para actualizar el nombre
    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UserProfessionUpdate(generics.UpdateAPIView):
    """ Api para actualizar el nombre
    """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class UserChangeEmail(generics.UpdateAPIView):
    """Api para actualizar el email de un usuario
    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        email = self.request.data.get('old_email')
        user = get_user_model().objects.get(email=email)
        try:
            obj = get_user_model().objects.get(pk=user.pk)
        except:
            raise ValidationError('No existe un usuario con ese correo')
        return obj


class UserChangePassword(generics.UpdateAPIView):
    """Api para actualizar el email de un usuario
    """

    serializer_class = ChangePasswordSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        email = self.request.data.get('email')
        user = User.objects.get(email=email)
        return user


class SectorList(generics.ListAPIView):
    """Api para listar los sectores disponibles para las empresas
    """

    serializer_class = SectorSerializer
    queryset = Sector.objects.all()


class CompanyUpdate(APIView):
    """Api para crear y/o actualizar la compañia de un usuario
    """

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        employees = request.POST['employees_number']
        sector_id = request.POST['sector']
        sector = Sector.objects.get(pk=sector_id)
        description = request.POST['description']
        user = User.objects.get(pk=request.POST['pk'])

        company = Company.objects.filter(user=user)
        if company:
            company = company.last()
            company.name = name
            company.employees_number = employees
            company.sector = sector
            company.description = description
            company.save()
        else:
            company = Company(
                name=name,
                employees_number=employees,
                sector=sector,
                description=description,
                user=user
            )
            company.save()

        response = {'detail': "Compañía actualizada exitosamente"}
        status_e = status.HTTP_201_CREATED
        return Response(response, status=status_e)
