from django.conf.urls import url
from django.urls import path, include
from .views import (
    DocumentExport,
    CategoryExport,
    DocumentBundleExport,
    InvoiceExport
)


app_name = 'reports'

urlpatterns = [
    path('document-sales/', DocumentExport.as_view(), name='document-sales'),
    path('category-sales/', CategoryExport.as_view(), name='category-sales'),
    path('documentbundle-sales/', DocumentBundleExport.as_view(), name='documentbundle-sales'),
    path('user-sales/', InvoiceExport.as_view(), name='user-sales'),
]