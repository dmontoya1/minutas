from django.contrib import admin
from utils.admin import SoftDeletionModelAdminMixin
from .models import (
    DocumentBundle,
    UserDocument
)


@admin.register(DocumentBundle)
class DocumentBundleAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
    )


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'created_at')