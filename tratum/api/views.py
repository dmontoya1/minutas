# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import APIKey
from .serializers import ApiKeySerializer


class ApiKeyDetailView(generics.ListAPIView):
    """
    API para obtener la api key
    """

    serializer_class = ApiKeySerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if APIKey.objects.filter(name='web').exists():
            serializer = ApiKeySerializer(APIKey.objects.get(name='web'), many=False)
        else:
            return Response({
                'detail': 'Ocurrió un error al obtener el objeto'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data)
