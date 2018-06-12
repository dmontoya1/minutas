from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path, include
from webclient.views import (
    HomePageView,
    DocumentDetailView,
    PoliciesView,
    FAQView,
    AboutUsView
)
from document_manager.views import ProcessDocumentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('policies/', PoliciesView.as_view(), name='policies'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('document/<slug:slug>/', DocumentDetailView.as_view(), name='document'),
    path('process/', ProcessDocumentView.as_view(), name='process'),
    path('business_info/', include('business_info.urls'), name='business_info'),
    path('store/', include('store.urls'), name='store'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns