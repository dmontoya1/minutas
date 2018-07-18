# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializador para los usuarios
    """

    class Meta:
        model = User
        fields = ('id', 'terms_and_conditions', 'email_validated')
