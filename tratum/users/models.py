# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    """Modelo para guardar los datos opcionales de la empresa
    de un usuario
    """

    name = models.CharField('Nombre Empresa', max_length=255)
    employees_number = models.IntegerField('Número de empleados')
    description = models.TextField('Descripción')
    sector = models.CharField('Sector', max_length=255)
    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        related_name='related_%(class)ss',
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