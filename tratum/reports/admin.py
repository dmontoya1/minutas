from django.contrib import admin
from django.db.models import Count
from .models import (
    DocumentSaleSummary,
    UserDocumentsSummary,
    BundleSaleSummary,
    CategorySaleSummary
)


@admin.register(DocumentSaleSummary)
class DocumentSaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/document_reports/documentsale_summary_change_list.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = qs
        
        return response


@admin.register(CategorySaleSummary)
class CategorySaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/category_reports/categorysales_summary_chage_list.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = qs
        
        return response


@admin.register(UserDocumentsSummary)
class UserDocumentsSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_reports/userdocuments_summary_chage_list.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = qs
        
        return response


@admin.register(BundleSaleSummary)
class BundleSaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/bundle_reports/bundlesales_summary_chage_list.html'

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = qs
        
        return response
    


