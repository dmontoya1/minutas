from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html


class SoftDeletionModelAdminMixin(admin.ModelAdmin):
    """Modeladmin para los modelos que hereden de SoftDeletionModelMixin.
    
    Atributos:
        exclude: Remueve el campo 'deleted_at' de la lista de objetos en el admin.
        actions: Se deja vacío para remover el borrado predeterminado de Django
        extra_list_display: Usado en el método get_list_display() para agregar los 
        campos específicos de cada ModelAdmin 

    """

    exclude = ('deleted_at',)
    actions = None
    extra_list_display = ()
    
    def response_change(self, request, obj):
        """Modifica la respuesta de las acciones en el template de edición de objeto para 
        procesar el botón de 'Inhabilitar'.
        """

        opts = self.model._meta
        custom_redirect = False

        if "_soft-delete" in request.POST:
            obj.soft_delete() 
            custom_redirect = True

        if "_revive" in request.POST:
            obj.revive() 
            custom_redirect = True

        if custom_redirect:
            redirect_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
            return HttpResponseRedirect(redirect_url)
        else:
             return super(SoftDeletionModelAdminMixin, self).response_change(request, obj)

    def is_alive(self, obj):
        """Método para evaluar si un objeto está inhabilitado o no y mostrar un 'check' en el 
        listado de objetos del admin.
        """

        icon = 'yes'
        if obj.deleted_at:
            icon = 'no'        
        return format_html(
            '<img src="/static/admin/img/icon-{icon}.svg" alt="{icon}">'.format(
                icon=icon
            )
        )
    is_alive.short_description = '¿Habilitado?'

    def get_list_display(self, request):
        """Modifica el 'list_display' predeterminado para mostrar siempre el estado de inhabilitación
        del objeto y los campos específicos de cada ModelAdmin, los cuales se agregan en 'extra_list_display'
        """

        return self.extra_list_display + ('is_alive', )  
    
    def get_queryset(self, request):
        qs = super(SoftDeletionModelAdminMixin, self).get_queryset(request)
        return qs

            
    

    