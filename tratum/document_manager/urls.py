from django.urls import path, include
from .views import (
    DocumentFieldList
)


urlpatterns = [
    path('document-fields/', DocumentFieldList.as_view(), name='document-fields')
]