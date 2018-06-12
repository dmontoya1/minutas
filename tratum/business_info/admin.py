from django.contrib import admin
from .models import (
    Policy,
    FAQCategory,
    FAQItem,
    SiteConfig
)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        'policy_type',
        'last_update_date'
    )


class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 0


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    inlines = [
        FAQItemInline
    ]


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        else:
            return True


