from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter, get_adapter
from allauth.account.utils import perform_login
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import LogTerms


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

        pass

