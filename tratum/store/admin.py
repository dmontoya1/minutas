from django.contrib import admin
from utils.admin import SoftDeletionModelAdminMixin
from .models import (
    DocumentBundle,
    UserDocument,
    Invoice
)


@admin.register(DocumentBundle)
class DocumentBundleAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
    )

@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document', 'created_at')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'payment_status')
    search_fields = ('payu_reference_code', )
