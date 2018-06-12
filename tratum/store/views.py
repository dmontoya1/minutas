from rest_framework import generics
from .models import DocumentBundle
from .serializers import DocumentBundleSerializer


class DocumentBundleList(generics.ListAPIView):
    queryset = DocumentBundle.objects.alive()
    serializer_class = DocumentBundleSerializer

