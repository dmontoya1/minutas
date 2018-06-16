from django.urls import path, include
from .views import (
    DocumentFieldList,
    DocumentSectionList,
    DocumentSectionDetail
)


urlpatterns = [
    path('document-fields/', DocumentFieldList.as_view(), name='document-fields'),
    path('document-sections/', DocumentSectionList.as_view(), name='document-sections'),
    path('document-sections/<slug:slug>/', DocumentSectionDetail.as_view(), name='document-section')
]