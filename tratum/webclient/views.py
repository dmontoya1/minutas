# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.models import Token

from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView

from business_info.models import (
    Policy,
    FAQCategory,
    SiteConfig
)
from document_manager.models import (
    Document,
    Category
)
from store.models import (
    DocumentBundle
)

from users.models import LogTerms


class HomePageView(TemplateView):

    template_name = "webclient/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bundles'] = DocumentBundle.objects.alive()
        context['categories'] = Category.objects.filter(deleted_at=None)
        return context


class PoliciesView(TemplateView):

    template_name = "webclient/policies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['policies'] = Policy.objects.all()
        return context


class FAQView(TemplateView):

    template_name = "webclient/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_categories'] = FAQCategory.objects.all()
        return context


class AboutUsView(TemplateView):

    template_name = "webclient/about_us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_config = SiteConfig.objects.last()
        if site_config:
            context['title'] = site_config.about_page_title
            context['content'] = site_config.about_page_content
            context['image'] = site_config.about_page_image
        return context


class DocumentDetailView(DetailView):

    model = Document


class LoginView(View):
    """Iniciar Sesión
    """

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            url = reverse('webclient:home')
            login(request, user)
        else:
            response = {'error': 'Correo y/o contraseña incorrectas.'}
            return JsonResponse(response, status=400)

        return JsonResponse(url, safe=False)


class SignupView(View):
	"""Clase para Registrar un usuario
	"""

	def post(self, request, *args, **kwargs):
		try:
			user = get_user_model()
			user = user()
			user.email = request.POST['email']
			user.username = request.POST['email']
			user.set_password(request.POST['password1'])
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			user.save()

			Token.objects.create(user=user)

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
			
			login(request, user)
			url = reverse('webclient:home')
			return JsonResponse(url, safe=False)
		except IntegrityError:
			msg = 'Tu correo ya está registrado. Por favor inicia sesión'
			response = {'error': msg}
			return JsonResponse(response, status=400)


class DocumentsView(TemplateView):

    template_name = "webclient/documents.html"
