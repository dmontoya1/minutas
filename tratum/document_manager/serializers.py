from rest_framework import serializers
from .models import DocumentField


class DocumentFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentField
        fields = ('name', 'clean_uuid')