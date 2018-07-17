from django.urls import path, include
from . import views


urlpatterns = [
    path('document-bundles/', views.DocumentBundleList.as_view(), name='document-bundles'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('confirmation/', views.Checkout.confirmation, name='checkout-confirmation'),
]