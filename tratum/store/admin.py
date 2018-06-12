from django.contrib import admin
from utils.admin import SoftDeletionModelAdminMixin
from .models import (
    DocumentBundle
)


@admin.register(DocumentBundle)
class DocumentBundleAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
    )