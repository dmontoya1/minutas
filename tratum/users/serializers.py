# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import check_password

from rest_framework import serializers

from .models import User, Sector


class UserSerializer(serializers.ModelSerializer):
    """Serializador para los usuarios
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'email',)


class ChangePasswordSerializer(serializers.ModelSerializer):
	"""Serializador para cambiar el password de un usuario
	"""

	class Meta:
		model = User
		fields = ('password',)

	def save(self):
		change_password = self.context['request'].data.get('password',None)
		if change_password != None:
			user = User.objects.get(
				email=self.context['request'].data['email']
			)
			if self.context['request'].data['old_password'] == change_password:
				raise serializers.ValidationError("La contraseña nueva es igual a la anterior, por favor verifica tu información")
			check = check_password(self.context['request'].data['old_password'], user.password)
			if check == True:
				user.set_password(self.context['request'].data['password'])
				user.save()
			else:
				raise serializers.ValidationError("La contraseña ingresada no corresponde a la de tu cuenta")
			return user
		super(ChangePasswordSerializer, self).save()


class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = ('id', 'name')
