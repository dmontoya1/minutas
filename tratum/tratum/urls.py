from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from document_manager.views import ProcessDocumentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('webclient.urls'), name='webclient'),
    path('api/', include('api.urls'), name="api"),
    path('business-info/', include('business_info.urls'), name='business_info'),
    path('store/', include('store.urls'), name='store'),
    path('document-manager/', include('document_manager.urls'), name='document_manager'),
    path('users/', include('users.urls'), name='users'),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns