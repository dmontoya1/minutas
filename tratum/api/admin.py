# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import messages
from .helpers import generate_key
from .models import APIKey

class ApiKeyAdmin(admin.ModelAdmin):
    """
    Clase para administrar las API Keys de la plataforma
    """
    list_display = ('key', 'name', 'created', 'modified')

    fieldsets = (
        ('Informacion Requerida', {'fields': ('name',)}),
        ('Informacion Adicional', {'fields': ('key_message',)}),
    )
    readonly_fields = ('key_message',)
    icon = '<i class="material-icons">https</i>'
    search_fields = ('id', 'name',)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def key_message(self, obj):
        return obj.key

    def save_model(self, request, obj, form, change):
        if not obj.key:
            obj.key = generate_key()
            messages.add_message(request, messages.WARNING, ('The API Key for %s is %s.' % (obj.name, obj.key)))
        obj.save()
admin.site.register(APIKey, ApiKeyAdmin)
