from rest_framework import serializers
from .models import DocumentBundle, UserDocument


class DocumentBundleSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentBundle
        fields = ('__all__')


class UserDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDocument
        fields = ('answers',)