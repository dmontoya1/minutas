from rest_framework import serializers
from .models import (
    DocumentField,
    DocumentSection
)


class DocumentFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentField
        fields = ('name', 'formated_slug')


class DocumentSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentSection
        fields = ('id', 'name', 'formated_slug', 'content')