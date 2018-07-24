# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.models import Token

from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template import loader
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView

from utils.views import account_activation_token

from business_info.models import (
    Policy,
    FAQCategory,
    SiteConfig,
    SliderItem
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
        context['context_bundles'] = DocumentBundle.objects.alive()
        context['context_slides'] = SliderItem.objects.all()
        return context


class PoliciesView(TemplateView):

    template_name = "webclient/policies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        police = get_object_or_404(Policy, policy_type='PP')
        context = super(PoliciesView, self).get_context_data(**kwargs)
        context['name'] = 'Política de privacidad y tratamiento de datos'
        context['content'] = police.content
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
        user = User.objects.get(username=email)
        print (user)
        if not user.is_active:
            response = {'error': 'Debes activar tu cuenta para continuar...'}
            return JsonResponse(response, status=400)
        else:
            user = authenticate(email=email, password=password)
            print (user)
            if user is not None:
                url = reverse('webclient:profile')
                login(request, user)
                messages.add_message(
                    request,
                        messages.ERROR, 
                        "Bienvenido de vuelta a Tratum"
                )
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
            user.is_active = False
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
            current_site = get_current_site(request)

            ctx = {
                'email': user.email,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'user_id': user.pk
            }
            body = loader.get_template('webclient/account_activation_email.html').render(ctx)
            message = EmailMessage("Activa tu cuenta en Tratum", body, 'no-reply@tratum.com', [user.email])
            message.content_subtype = 'html'
            message.send()

            messages.add_message(
                request,
                    messages.ERROR, 
                    "Te has registrado correctamente. Revisa tu correo para activar tu cuenta"
            )
            url = reverse('webclient:home')
            return JsonResponse(url, safe=False)
        except IntegrityError:
            msg = 'Tu correo ya está registrado. Por favor inicia sesión'
            response = {'error': msg}
            return JsonResponse(response, status=400)


class CategoryDocumentsView(TemplateView):

    template_name = "webclient/documents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        categories = category.get_descendants(include_self=True)
        context['category'] = category
        context['documents'] = Document.objects.filter(category__in=categories).order_by('order')
        return context


class ProfileView(TemplateView):

    template_name = "webclient/profile.html"


def activate(request, uidb64, token, pk):
    try:
        user = User.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print (user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)
        messages.add_message(
            request,
                messages.ERROR, 
                "Has activado tu cuenta exitosamente."
        )
        return redirect('webclient:home')
    else:
        messages.add_message(
            request,
                messages.ERROR, 
                "No hemos podido activar tu cuenta, "
        )
        return redirect('webclient:home')
