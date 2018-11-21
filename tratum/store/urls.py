from django.urls import path

from . import views


app_name = 'store'
urlpatterns = [
    path('document-bundles/', views.DocumentBundleList.as_view(), name='document-bundles'),
    path('create-user-document/', views.CreateUserDocument.as_view(), name='create-user-document'),
    path('user-document/<slug:identifier>/', views.UserDocumentDetailView.as_view(), name='user-document'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('confirmation/', views.Checkout.confirmation, name='checkout-confirmation'),
]
