from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from utils.admin import SoftDeletionModelAdminMixin
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
            '/static/js/admin/maskComponent.js'
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
        'name',
        'document',
        'section',
        'field_type',
        'slug'
    )
    list_filter = (
        'document',
        'section',
        'field_type'
    )
    readonly_fields = ('slug',)
    
    def get_form(self, request, obj=None, **kwargs):
        request.current_object = obj
        return super(DocumentFieldAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        obj = request.current_object
        filters = {}
        if obj:
            if obj.document:
                filters['document__pk'] = obj.document.pk
            else:
                filters['section__pk'] = obj.section.pk
            if db_field.name == "field_group":
                kwargs["queryset"] = DocumentField.objects.filter(**filters).exclude(field_type=DocumentField.GROUP)
        return super(DocumentFieldAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = (
            '/static/js/admin/documentfields.js',
        )

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
