from rest_framework import serializers
from .models import (
    DocumentField,
    DocumentSection,
    Document, 
    Category
)


class FieldGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentField
        fields = ('formated_slug',)

class DocumentFieldSerializer(serializers.ModelSerializer):
    field_group = FieldGroupSerializer(source='get_ordered_group_fields', many=True)

    class Meta:
        model = DocumentField
        fields = ('name', 'field_type', 'formated_slug', 'group_expression', 'field_group')


class DocumentSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentSection
        fields = ('id', 'name', 'formated_slug', 'content')


class CategorySerializer(serializers.ModelSerializer):

    url = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = Category
        fields = ('id','name', 'slug', 'url')


class DocumentSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = Document
        fields = ('id', 'name', 'short_description', 'long_description', 'category', 'price', 'video_url' )
