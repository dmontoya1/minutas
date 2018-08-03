from django.contrib import admin
from django.db.models import Count
from .models import DocumentSaleSummary



@admin.register(DocumentSaleSummary)
class DocumentSaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/document_reports/documentsale_summary_change_list.html'
    actions = ['export_csv']

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
    
    
