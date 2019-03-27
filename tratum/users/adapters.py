import logging
import mimetypes

from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter, get_adapter
from allauth.account.utils import perform_login
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import LogTerms

from tratum.business_info.models import SiteConfig


logger = logging.getLogger(__name__)


class AccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        return reverse('webclient:confirm-email')

    def save_user(self, request, user, form, commit=False):
        data = form.cleaned_data

        user.email = data['email']
        user.user_type = 'PC'
        user.username = data['email']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        user.save()
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
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request):
        return reverse('webclient:profile')

    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()
        u.email_validated = True
        u.save()
        if form:
            get_adapter().save_user(request, u, form)
        else:
            get_adapter().populate_username(request, u)
        sociallogin.save(request)

        return redirect(reverse('webclient:profile'))

    def pre_social_login(self, request, sociallogin):
        existing_user = True
        try:
            user = get_user_model().objects.get(email=sociallogin.user.email)
        except get_user_model().DoesNotExist:
            existing_user = False

        if existing_user:
            if not sociallogin.is_existing:
                sociallogin.connect(request, user)
            return perform_login(request, user, app_settings.EMAIL_VERIFICATION)
        else:
            try:
                ctx = dict(
                    name=sociallogin.user.first_name
                )
                body = loader.get_template('webclient/email/welcome_email.html').render(ctx)
                email = EmailMessage(
                    "Bienvenido a Tratum",
                    body,
                    'no-reply@tratum.co',
                    [sociallogin.user.email]
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
