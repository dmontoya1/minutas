# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests
import mimetypes

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import redirect, get_object_or_404, reverse
from django.template import Template, Context, loader
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from allauth.socialaccount.models import SocialAccount
from rest_framework.authtoken.models import Token

from tratum.utils.views import account_activation_token

from tratum.business_info.models import (
    Policy,
    SiteConfig
)
from tratum.document_manager.models import (
    Document,
    Category
)
from tratum.store.models import UserDocument

from tratum.users.models import LogTerms


logger = logging.getLogger(__name__)


class HomePageView(TemplateView):

    template_name = "webclient/home.html"


class PoliciesView(TemplateView):

    template_name = "webclient/policies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _type = self.kwargs.get('type', 'PP')
        pdf_url = None
        site_conf = SiteConfig.objects.last()
        if _type:
            if self.kwargs['type'] == 'privacy':
                _type = 'PP'
                if site_conf:
                    pdf_url = site_conf.data_policy_file.url
            elif self.kwargs['type'] == 'terms':
                _type = 'TCP'
                if site_conf:
                    pdf_url = site_conf.terms_file.url
            elif self.kwargs['type'] == 'cookies':
                _type = 'CMP'
        police = get_object_or_404(Policy, policy_type=_type)
        context = super(PoliciesView, self).get_context_data(**kwargs)
        context['name'] = police.get_policy_type_display()
        context['content'] = police.content
        context['pdf_url'] = pdf_url
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


class FAQView(TemplateView):

    template_name = "webclient/faq.html"


class GlossaryView(TemplateView):

    template_name = "webclient/glossary.html"


class DocumentDetailView(DetailView):

    model = Document


class LoginView(View):
    """Iniciar Sesi??n"""
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        next = request.POST.get('email_login_next', False)

        if SocialAccount.objects.filter(user__email=email).count() > 0:
            response = {'error': 'La cuenta con la que intentas iniciar est?? conectada a una red social'}
            return JsonResponse(response, status=400)
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            response = {'error': 'El correo no se encuentra registrado en la plataforma'}
            return JsonResponse(response, status=400)
        if not user.is_active:
            response = {'error': 'Debes activar tu cuenta para continuar...'}
            return JsonResponse(response, status=400)
        else:
            user = authenticate(email=email, password=password)
            if user is not None:
                url = next if next else reverse('webclient:profile')
                login(request, user)
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Bienvenido de vuelta a Tratum"
                )
            else:
                response = {'error': 'Correo y/o contrase??a incorrectas.'}
                return JsonResponse(response, status=400)

            return JsonResponse(url, safe=False)


class SignupView(View):
    """Clase para Registrar un usuario
    """

    def post(self, request, *args, **kwargs):
        try:
            user = get_user_model()
            user = user()
            if SocialAccount.objects.filter(user__email=request.POST['email']).count() > 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Ya existe una cuenta registrada con ??ste correo electr??nico conectado a una red social."
                )
            else:
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
                    'token': account_activation_token.make_token(user),
                    'user_id': user.pk
                }
                body = loader.get_template('webclient/email/account_activation_email.html').render(ctx)
                message = EmailMessage(
                    "Activa tu cuenta en Tratum",
                    body,
                    'no-reply@tratum.co',
                    [user.email]
                )
                message.content_subtype = 'html'
                message.send()

                messages.add_message(
                    request,
                    messages.ERROR,
                    "Te has registrado correctamente. Revisa tu correo para activar tu cuenta"
                )
            next_url = request.POST.get('email_signup_next', False)
            url = next_url if next_url else reverse('webclient:home')
            return JsonResponse(url, safe=False)
        except IntegrityError:
            msg = 'Tu correo ya est?? registrado. Por favor inicia sesi??n'
            response = {'error': msg}
            return JsonResponse(response, status=400)


class ValidateTerms(LoginRequiredMixin, TemplateView):

    login_url = '/'
    redirect_field_name = 'next'
    template_name = 'webclient/validate_terms.html'

    def get_context_data(self, **kwargs):
        terms = get_object_or_404(Policy, policy_type='TCP')
        police = get_object_or_404(Policy, policy_type='PP')
        user = self.request.user
        try:
            user_token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            user_token = Token(
                user=user
            )
            user_token.save()
        context = super(ValidateTerms, self).get_context_data(**kwargs)
        context['terms_name'] = terms.get_policy_type_display()
        context['terms_content'] = terms.content
        context['police_name'] = police.get_policy_type_display()
        context['police_content'] = police.content
        context['user'] = user
        context['user_token'] = user_token
        return context


class CategoryDocumentsView(TemplateView):

    template_name = "webclient/documents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        categories = category.get_descendants(include_self=True).alive()
        context['category'] = category
        context['documents'] = Document.objects.alive().filter(category__in=categories).order_by('order')
        return context


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "webclient/profile.html"
    login_url = '/'


class UserDocumentsView(LoginRequiredMixin, ListView):
    model = UserDocument
    template_name = "webclient/user_documents.html"
    login_url = '/'
    redirect_field_name = 'next'

    def get_queryset(self):
        docs = UserDocument.objects.filter(user=self.request.user)
        docs_list = []
        for doc in docs:
            if not doc.is_expired():
                docs_list.append(doc)
        return docs_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        user = request.user
        if not self.object_list:
            messages.add_message(
                request,
                messages.ERROR,
                "No tienes documentos creados. \
                Crea o compra tu primer documento desde aqu??"
            )
            return redirect(reverse('webclient:category_documents', args=("",)))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class UserDocumentView(LoginRequiredMixin, DetailView):
    model = UserDocument
    template_name = "document_form/document_detail.html"
    slug_field = "identifier"
    login_url = '/'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_file_document():
            filename = obj.file.name.split('/')[-1]
            response = HttpResponse(obj.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        return super().get(request, *args, **kwargs)

    def get_object(self):
        user_document = get_object_or_404(
            UserDocument,
            identifier=self.kwargs['identifier'],
            user=self.request.user
        )
        return user_document.document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['identifier'] = self.kwargs['identifier']
        return context


class UserDocumentPreviewView(DetailView):
    model = UserDocument
    template_name = "document_form/document_preview.html"
    slug_field = "identifier"

    def get_object(self):
        return get_object_or_404(
            UserDocument,
            identifier=self.kwargs['identifier'],
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        doc_content = "{% load fieldformatter %}" + obj.document.content
        document_content = Template(doc_content)
        document_content = document_content.render(Context(obj.answers))
        context['document_content'] = document_content
        return context


class UserDocumentProcessPreviewView(View):
    model = UserDocument
    slug_field = "identifier"

    def get_object(self):
        return get_object_or_404(
            UserDocument,
            identifier=self.kwargs['identifier'],
            user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        preview = reverse('webclient:user-document-preview', kwargs={'identifier': obj.identifier})
        return HttpResponseRedirect(preview)


class ContactFormView(View):
    """Mensajes del formulario de contacto y solicitud de documentos
    """

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        topic = 'Mensaje de {name} desde el formulario de Tratum'.format(name=name)

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if result['success']:
            if request.POST.get('is_document', None):
                topic = 'Solicitud de nuevo documento de {name} desde Tratum'.format(name=name)
            email = EmailMessage(
                topic,
                '{email} env??a esto: {message}'.format(
                    email=email,
                    message=message
                ),
                'no-reply@tratum.co',
                ['czuniga@ilanalab.com']
            )
            email.send()
            messages.add_message(request, messages.SUCCESS, "Mensaje env??ado correctamente")
            return JsonResponse(dict(message="Mensaje env??ado correctament"))
        else:
            return JsonResponse(dict(error="No se complet?? correctamente el captcha"), status=400)


def activate(request, token, pk):
    try:
        user = User.objects.get(pk=pk)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
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

        try:
            ctx = dict(
                name=user.first_name
            )
            body = loader.get_template('webclient/email/welcome_email.html').render(ctx)
            email = EmailMessage(
                "Bienvenido a Tratum",
                body,
                'no-reply@tratum.co',
                [user.email]
            )
            email.content_subtype = 'html'

            site_config = SiteConfig.objects.last()

            if site_config:
                content_type = mimetypes.guess_type(site_config.terms_file.name)[0]
                email.attach(site_config.terms_file.name, site_config.terms_file.read(), content_type)

                content_type2 = mimetypes.guess_type(site_config.data_policy_file.name)[0]
                email.attach(site_config.data_policy_file.name, site_config.data_policy_file.read(), content_type2)

            email.send()

        except Exception as e:
            logger.exception(str(e))

        return redirect('webclient:home')
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "No hemos podido activar tu cuenta, "
        )
        return redirect('webclient:home')


class CreacionEmpresa(TemplateView):
    template_name = 'landings/creacion_empresa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name='Creaci??n de Empresa')
        documents = Document.objects.filter(category=category, is_active=True)[:6]
        context['documents'] = documents
        context['category'] = category
        return context


class GestionContractual(TemplateView):
    template_name = 'landings/gestion_contractual.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name='Gesti??n contractual')
        documents = Document.objects.filter(category=category, is_active=True)[:6]
        context['documents'] = documents
        context['category'] = category
        return context


class GestionEmpresarial(TemplateView):
    template_name = 'landings/gestion_empresarial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name='Gesti??n empresarial')
        documents = Document.objects.filter(category=category, is_active=True)[:6]
        context['documents'] = documents
        context['category'] = category
        return context


class NegociosAsuntosPersonales(TemplateView):
    template_name = 'landings/negocios_asuntos_personales.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name='Negocios y asuntos personales')
        documents = Document.objects.filter(category=category, is_active=True)[:6]
        context['documents'] = documents
        context['category'] = category
        return context


class LandingForm(TemplateView):
    template_name = 'landings/landing_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def send_contact_email(request):
    data = request.POST
    ctx = {
        'email': data['email'],
        'name': data['name'],
        'phone': data['phone']
    }
    body = loader.get_template('webclient/email/contact_email.html').render(ctx)
    message = EmailMessage(
        "Mensaje de contacto",
        body,
        'no-reply@tratum.co',
        [settings.ADMIN_EMAIL]
    )
    message.content_subtype = 'html'
    message.send()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Tu mensaje ha sido enviado correctamente"
    )
    return HttpResponseRedirect(reverse('webclient:home'))


def send_register_email(request):
    data = request.POST
    ctx = {
        'email': data['email'],
        'name': data['name'],
        'phone': data['phone']
    }
    body = loader.get_template('webclient/email/contact_email.html').render(ctx)
    message = EmailMessage(
        "Mensaje de Registro Evento",
        body,
        'no-reply@tratum.co',
        ['czuniga.lab@gmail.com', 'pgutierrez.lab@gmail.com']
        # ['dmontoya.lab@gmail.com']
    )
    message.content_subtype = 'html'
    message.send()

    messages.add_message(
        request,
        messages.SUCCESS,
        "Te has registrado con exito"
    )
    return HttpResponseRedirect(reverse('webclient:home'))
