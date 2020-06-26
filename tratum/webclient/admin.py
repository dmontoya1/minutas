from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin, ExportMixin


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class UserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = UserResource


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
