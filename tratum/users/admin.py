# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Company, LogTerms, Sector


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
