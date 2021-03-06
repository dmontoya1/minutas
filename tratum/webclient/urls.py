import mptt_urls

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

from tratum.document_manager.models import Category
from tratum.document_manager.views import category


app_name = 'webclient'
urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='home'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page="/"),
        name='logout'
    ),
    path(
        'signup/',
        views.SignupView.as_view(),
        name='signup'
    ),
    path(
        'policies/<str:type>/',
        views.PoliciesView.as_view(),
        name='policies'
    ),
    path(
        'validate-terms/',
        views.ValidateTerms.as_view(),
        name="validate-terms"
    ),
    path(
        'faq/',
        views.FAQView.as_view(),
        name="faq"
    ),
    path(
        'glosario/',
        views.GlossaryView.as_view(),
        name="glossary"
    ),
    path(
        'about-us/',
        views.AboutUsView.as_view(),
        name='about-us'
    ),
    path(
        'my-documents/<slug:identifier>/edit/',
        views.UserDocumentView.as_view(),
        name='user-document'
    ),
    path(
        'my-documents/<slug:identifier>/process/',
        views.UserDocumentProcessPreviewView.as_view(),
        name='user-document-process'
    ),
    path(
        'my-documents/<slug:identifier>/preview/',
        views.UserDocumentPreviewView.as_view(),
        name='user-document-preview'
    ),
    path(
        'profile/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'my-documents/',
        views.UserDocumentsView.as_view(),
        name='user-documents'
    ),
    path(
        'activate/<token>/<pk>/',
        views.activate,
        name='activate'
    ),
    path(
        'contact-form/',
        views.ContactFormView.as_view(),
        name='contact-form'
    ),
    url(
        r'^documents/(?P<path>.*)',
        mptt_urls.view(model=Category, view=category, slug_field='slug'),
        name='category_documents'
    ),
    path(
        'creacion-empresa/',
        views.CreacionEmpresa.as_view(),
        name="creacion_empresa"
    ),
    path(
        'gestion-contractual/',
        views.GestionContractual.as_view(),
        name="gestion_contractual"
    ),
    path(
        'gestion-empresarial/',
        views.GestionEmpresarial.as_view(),
        name="gestion_empresarial"
    ),
    path(
        'negocios-asuntos-personales/',
        views.NegociosAsuntosPersonales.as_view(),
        name="negocios_asuntos_personales"
    ),
    path(
        'contact-form-landing/',
        views.send_contact_email,
        name="contact_form_email"
    ),
    path(
        'register-form-landing/',
        views.send_register_email,
        name="register_email"
    ),
    path(
        'registro-evento/',
        views.LandingForm.as_view(),
        name="landing_form"
    ),
]
