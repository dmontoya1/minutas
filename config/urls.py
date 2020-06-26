from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views


urlpatterns = [

    # Admin
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path(settings.ADMIN_URL, admin.site.urls),

    path("accounts/", include("allauth.urls")),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),

    path('', include('tratum.webclient.urls'), name='webclient'),
    path('api/', include('tratum.api.urls'), name="api"),
    path('business-info/', include('tratum.business_info.urls'), name='business_info'),
    path('chaining/', include('smart_selects.urls')),
    path('document-manager/', include('tratum.document_manager.urls'), name='document_manager'),
    path('reports/', include('tratum.reports.urls', namespace='reports')),
    path('store/', include('tratum.store.urls'), name='store'),
    path('users/', include('tratum.users.urls'), name='users'),

] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
