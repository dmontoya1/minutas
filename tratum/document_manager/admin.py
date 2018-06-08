from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from utils.admin import SoftDeletionModelAdminMixin
from .models import Document, Category


@admin.register(Document)
class DocumentAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
        'category'
    ) 
    list_select_related = (
        'category',
    )
    readonly_fields = ('slug',)

@admin.register(Category)
class CategoryAdmin(SoftDeletionModelAdminMixin, MPTTModelAdmin):
    extra_list_display = (
        'name',
        'parent'
    )

