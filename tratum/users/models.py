# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Sector(models.Model):
    """Modelo para guar el sector de las compañías
    """
    name = models.CharField("Sector", max_length=255)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"

    def __str__(self):
        return self.name


class Company(models.Model):
    """Modelo para guardar los datos opcionales de la empresa
    de un usuario
    """

    EMPLOYEE_CHOICES = (
		(1, 'Menos de 10'),
		(2, 'Entre 10 y 20'),
		(3, 'Entre 20 y 50'),
		(4, 'Más de 50'),
	)

    name = models.CharField('Nombre Empresa', max_length=255)
    employees_number = models.IntegerField(
        'Número de empleados',
        choices=EMPLOYEE_CHOICES,
        blank=True,
        null=True
    )
    
    description = models.TextField('Descripción')
    sector = models.ForeignKey(
        Sector,
        verbose_name="Sector",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    user = models.OneToOneField(
        User,
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Compañía"

    def __str__(self):
        return self.name



class LogTerms(models.Model):
    """Modelo para guardar el log de los usuarios cuando aceptan los terminos
    """

    date = models.DateTimeField("Fecha", auto_now=True)
    ip = models.GenericIPAddressField("Dirección IP", protocol='both')
    user = models.ForeignKey(
        User,
        verbose_name="Usuario",
        related_name="related_log_terms",
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Log de términos"
        verbose_name_plural = "Logs de Términos"


    def __str__(self):
        return "%s" %(self.user)