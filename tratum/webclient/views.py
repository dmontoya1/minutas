# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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


class HomePageView(TemplateView):

    template_name = "webclient/home.html"


class PoliciesView(TemplateView):

    template_name = "webclient/policies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _type = self.kwargs.get('type', 'PP')
        if _type:
            if self.kwargs['type'] == 'privacy':
                _type = 'PP'
            elif self.kwargs['type'] == 'terms':
                _type = 'TCP'
            elif self.kwargs['type'] == 'cookies':
                _type = 'CMP'
        police = get_object_or_404(Policy, policy_type=_type)
        context = super(PoliciesView, self).get_context_data(**kwargs)
        context['name'] = police.get_policy_type_display()
        context['content'] = police.content
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


class DocumentDetailView(DetailView):

    model = Document


class LoginView(View):
    """Iniciar Sesión
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        print("LOGIN VIEW")

        if SocialAccount.objects.filter(user__email=email).count() > 0:
            response = {'error': 'La cuenta con la que intentas iniciar está conectada a una red social'}
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
            if SocialAccount.objects.filter(user__email=request.POST['email']).count() > 0:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Ya existe una cuenta registrada con éste correo electrónico conectado a una red social."
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
            url = reverse('webclient:home')
            return JsonResponse(url, safe=False)
        except IntegrityError:
            msg = 'Tu correo ya está registrado. Por favor inicia sesión'
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
        return docs

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            pass
        else:
            user = request.user
            docs = UserDocument.objects.filter(user=user)
            if not docs:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "No tienes documentos creados. \
                    Crea o compra tu primer documento desde aquí"
                )
                return redirect(reverse('webclient:category_documents', args=("",)))
        self.object_list = self.get_queryset()
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
        obj = UserDocument.objects.get(identifier=self.kwargs['identifier'])
        return obj.document

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['identifier'] = UserDocument.objects.get(identifier=self.kwargs['identifier']).identifier
        return context


class UserDocumentPreviewView(DetailView):
    model = UserDocument
    template_name = "document_form/document_preview.html"
    slug_field = "identifier"

    def get_object(self):
        obj = UserDocument.objects.get(identifier=self.kwargs['identifier'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        document_content = Template(obj.document.content)
        document_content = document_content.render(Context(obj.answers))
        context['document_content'] = document_content
        return context


class UserDocumentProcessPreviewView(View):
    model = UserDocument
    slug_field = "identifier"

    def get_object(self):
        obj = UserDocument.objects.get(identifier=self.kwargs['identifier'])
        return obj

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
        if request.POST.get('is_document', None):
            topic = 'Solicitud de nuevo documento de {name} desde Tratum'.format(name=name)
        email = EmailMessage(
            topic,
            '{email} envía esto: {message}'.format(
                email=email,
                message=message
            ),
            'no-reply@tratum.co',
            ['nrodriguez@apptitud.com.co']
        )
        email.send()
        messages.success(request, 'Mensaje envíado correctamente')
        return redirect('webclient:home')


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
        return redirect('webclient:home')
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "No hemos podido activar tu cuenta, "
        )
        return redirect('webclient:home')
