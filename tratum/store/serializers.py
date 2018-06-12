from rest_framework import serializers
from .models import DocumentBundle


class DocumentBundleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentBundle
        fields = ('__all__')