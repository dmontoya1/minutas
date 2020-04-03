# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .models import Company, LogTerms, Sector

User = get_user_model()


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    """Administrador para las compañías
    """
    model = Sector


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


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    list_display = ('email', 'first_name', 'last_name', 'date_joined')
