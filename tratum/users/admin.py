# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as django_user_admin
from django.contrib.auth.forms import UserChangeForm as django_change_form
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Company, LogTerms


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Administrador para las compañías
    """
    
    model = Company


@admin.register(LogTerms)
class LogTermsAdmin(admin.ModelAdmin):
    """Administrador para el Log de la aceptación de Terminos
    """

    model = LogTerms
    icon = '<i class="material-icons">gavel</i>'
    list_display = (
        'date', 'ip', 'user',
    )
    search_fields = (
        'date', 'ip', 'user_email',
    )
