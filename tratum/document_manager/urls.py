from django.urls import path, include
from .views import (
    DocumentFieldList,
    DocumentFieldDetail,
    DocumentSectionList,
    DocumentSectionDetail,
    DocumentSectionFieldsList,
    ProcessDocumentView,
    SaveAnswersView,
    DocumentList,
    CategoryRootList,
    CategoryChildrenList,
    FinishDocumentView,
    UserDocumentContentView,
    MainDocumentList,
    LinkedFieldView
)

app_name = 'document_manager'

urlpatterns = [
    path('document-fields/', DocumentFieldList.as_view(), name='document-fields'),
    path('document-fields/<slug:slug>/', DocumentFieldDetail.as_view(), name='document-field'),
    path('document-sections/', DocumentSectionList.as_view(), name='document-sections'),
    path('document-sections/<slug:slug>/', DocumentSectionDetail.as_view(), name='document-section'),
    path('document-options/<int:pk>/linked-fields/', LinkedFieldView.as_view(), name='document-option'),
    path('finish/', FinishDocumentView.as_view(), name='finish'),
    path('process/', ProcessDocumentView.as_view(), name='process'),
    path('save-preview/', SaveAnswersView.as_view(), name='save-preview'),
    path('form-preview/', UserDocumentContentView.as_view(), name='form-preview'),
    path('finish/', FinishDocumentView.as_view(), name='finish'),
    path('documents/', MainDocumentList.as_view(), name='main-document-list'),
    path('documents/<slug:slug>/', DocumentList.as_view(), name='document-list'),
    path('categories/', CategoryRootList.as_view(), name='categories-root-list'),
    path('categories/<slug:slug>/children/', CategoryChildrenList.as_view(), name='categories-children-list'),
]