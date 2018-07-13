
from django.urls import path, include
from .views import (
    HomePageView,
    DocumentDetailView,
    PoliciesView,
    FAQView,
    AboutUsView,
    SignupView
)

app_name = 'webclient'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('policies/', PoliciesView.as_view(), name='policies'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('document/<slug:slug>/', DocumentDetailView.as_view(), name='document'),
]