from django.contrib import admin
from django.urls import path, include
from webclient.views import HomePageView, DocumentDetailView
from document_manager.views import ProcessDocumentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('document/<slug:slug>/', DocumentDetailView.as_view(), name='document'),
    path('process/', ProcessDocumentView.as_view(), name='process'),
]
