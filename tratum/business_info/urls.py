from django.urls import path
from .views import (
    PolicyList,
    FAQCategoryList
)


urlpatterns = [
    path('policies/', PolicyList.as_view(), name='policies'),
    path('faq/', FAQCategoryList.as_view(), name='faq')
]
