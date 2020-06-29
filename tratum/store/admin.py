from django.contrib import admin

from tratum.utils.admin import SoftDeletionModelAdminMixin

from .models import (
    DocumentBundle,
    UserDocument,
    Invoice,
    Subscription,
    UserSubscription,
    UserDocumentsSubscription
)


@admin.register(DocumentBundle)
class DocumentBundleAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
    )


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_filter = ('user', 'document')
    list_display = ('user', 'document', 'created_at', 'identifier')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'payment_status', 'payu_reference_code')
    search_fields = ['payu_reference_code', 'user__email']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    """

    list_filter = ('name', 'document_number',)
    list_display = ('name', 'document_number', 'price',)


class UserDocumentsSubscriptionInline(admin.StackedInline):
    """
    """

    model = UserDocumentsSubscription
    extra = 0
    readonly_fields = ('user_document', 'date_added')


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """
    """

    list_display = ("user", "subscription", "status", "date_purchase",)
    list_filter = ("user", "subscription", "status")
    inlines = [UserDocumentsSubscriptionInline, ]
