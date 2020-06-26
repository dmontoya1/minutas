from django.contrib import admin

from .forms import SliderItemForm, SiteConfigForm
from .models import (
    Policy,
    FAQCategory,
    FAQItem,
    SiteConfig,
    SliderItem,
    GlossaryCategory,
    GlossaryItem,
    MainCategory
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


class GlossaryItemInline(admin.StackedInline):
    model = GlossaryItem
    extra = 0


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    inlines = [
        GlossaryItemInline
    ]


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    form = SiteConfigForm

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        else:
            return True


@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    form = SliderItemForm

    def has_add_permission(self, request):
        if self.model.objects.count() > 4:
            return False
        else:
            return True


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
