from django.contrib import admin
from django.utils.html import format_html

from mptt.admin import MPTTModelAdmin

from tratum.utils.admin import SoftDeletionModelAdminMixin

from .models import (
    Document,
    Category,
    DocumentField,
    DocumentSection,
    DocumentFieldOption
)


@admin.register(Document)
class DocumentAdmin(SoftDeletionModelAdminMixin):
    extra_list_display = (
        'name',
        'category',
        'price',
        'order'
    )
    list_select_related = (
        'category',
    )
    readonly_fields = ('slug', 'template_path')

    class Media:
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/mark.js/8.11.1/mark.min.js',
            '//unpkg.com/axios/dist/axios.min.js',
            # '/static/js/admin/maskComponent.js'
        )


@admin.register(Category)
class CategoryAdmin(SoftDeletionModelAdminMixin, MPTTModelAdmin):
    extra_list_display = (
        'name',
        'parent'
    )
    readonly_fields = ('slug', )


@admin.register(DocumentField)
class DocumentFieldAdmin(admin.ModelAdmin):
    list_display = (
        'document',
        'name',
        'display_name',
        'field_type',
        'orden'
    )
    list_filter = (
        'document',
        'section',
        'field_type'
    )
    readonly_fields = ('slug',)

    def get_form(self, request, obj=None, **kwargs):
        request.current_object = obj
        form = super(DocumentFieldAdmin, self).get_form(request, obj, **kwargs)
        if request.GET.get('document_id', None):
            form.base_fields['document'].queryset = Document.objects.filter(pk=request.GET['document_id'])
        if request.GET.get('section_id', None):
            form.base_fields['section'].queryset = DocumentSection.objects.filter(pk=request.GET['section_id'])
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        obj = request.current_object
        filters = {}
        if obj:
            if obj.document:
                filters['document__pk'] = obj.document.pk
            else:
                filters['section__pk'] = obj.section.pk
            if db_field.name == "field_group":
                kwargs["queryset"] = DocumentField.objects.filter(**filters)
        return super(DocumentFieldAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def orden(self, obj):
        return format_html(
            "<form method='POST' action='/update_order/'> \
                <input type='number' value='{}' name='order' class='order_number'> \
                <input type='hidden' value='{}' name='field_pk'> \
                <input type='button' value='Cambiar' class='changer_submit'> \
            </form>".format(obj.order, obj.pk)
        )

    class Media:
        js = (
            '/static/js/admin/documentfields.js',
        )
        css = {
            'all': ('/static/css/documentfields.css',)
        }


@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'document',
        'slug'
    )
    readonly_fields = ('slug',)

    class Media:
        js = (
            '//unpkg.com/axios/dist/axios.min.js',
        )


@admin.register(DocumentFieldOption)
class DocumentFieldOptionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'field'
    )

    list_filter = (
        'document',
        'field',
    )

    #filter_horizontal = ['linked_fields']
