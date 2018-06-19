from django.urls import path, include
from .views import (
    DocumentFieldList,
    DocumentSectionList,
    DocumentSectionDetail,
    DocumentSectionFieldsList
)


urlpatterns = [
    path('document-fields/', DocumentFieldList.as_view(), name='document-fields'),
    path('document-sections/', DocumentSectionList.as_view(), name='document-sections'),
    path('document-sections/<slug:slug>/', DocumentSectionDetail.as_view(), name='document-section'),
    path('document-sections/<slug:slug>/section-fields/', DocumentSectionFieldsList.as_view(), name='document-section-fields')
]