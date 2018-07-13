from rest_framework import serializers
from .models import APIKey

class ApiKeySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo de ApiKey
    """

    class Meta:
        model = APIKey
        fields = ('key',)
