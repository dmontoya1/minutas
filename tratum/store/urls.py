from django.urls import path, include
from .views import (
    DocumentBundleList
)


urlpatterns = [
    path('document-bundles/', DocumentBundleList.as_view(), name='document-bundles')
]