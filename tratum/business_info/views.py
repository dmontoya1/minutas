from rest_framework import generics
from .models import (
    Policy,
    FAQCategory
)
from .serializers import (
    PolicySerializer,
    FAQCategorySerializer
)


class PolicyList(generics.ListAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class FAQCategoryList(generics.ListAPIView):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer