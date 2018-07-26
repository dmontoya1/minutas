from django.urls import path, include
from .views import (
    DocumentFieldList,
    DocumentSectionList,
    DocumentSectionDetail,
    DocumentSectionFieldsList,
    ProcessDocumentView,
    SaveAnswersView,
    DocumentList,
    CategoryRootList,
    CategoryChildrenList
)

app_name = 'document_manager'

urlpatterns = [
    path('document-fields/', DocumentFieldList.as_view(), name='document-fields'),
    path('document-sections/', DocumentSectionList.as_view(), name='document-sections'),
    path('document-sections/<slug:slug>/', DocumentSectionDetail.as_view(), name='document-section'),
    path('document-sections/<slug:slug>/section-fields/', DocumentSectionFieldsList.as_view(), name='document-section-fields'),
    path('process/', ProcessDocumentView.as_view(), name='process'),
    path('save-preview/', SaveAnswersView.as_view(), name='save-preview'),
    path('documents/<slug:slug>/', DocumentList.as_view(), name='document-list'),
    path('categories/', CategoryRootList.as_view(), name='categories-root-list'),
    path('categories/<slug:slug>/children/', CategoryChildrenList.as_view(), name='categories-children-list'),
]