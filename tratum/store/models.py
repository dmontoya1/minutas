# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import datetime
import time

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.urls import reverse

from utils.models import SoftDeletionModelMixin

from document_manager.models import Document


class DocumentBundle(SoftDeletionModelMixin):
    """Guarda los paquetes de documentos para el módulo ecommerce.

    Campos del modelo:
        name: Nombre del paquete
        documents: Documentos incluídos en el paquete
    """

    name = models.CharField(
        'Nombre',
        max_length=50,
        unique=True
    )
    documents = models.ManyToManyField(
        Document,
        verbose_name='Documentos',
        blank=True
    )
    price = models.PositiveIntegerField('Precio')
    show_on_landing = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(
        'Orden',
        null=True,
        blank=True,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paquete de documento'   
        verbose_name_plural = 'Paquetes de documentos'

    def clean(self):
        """Retorna ValidationError si se intenta crear más tres instancias para la landing
        """

        model = self.__class__
        if (model.objects.filter(show_on_landing=True).exclude(pk=self.pk).count() >= 3 and 
                self.show_on_landing is True):
            raise ValidationError(
                "Sólo se puede agregar 3 paquetes a la landing.")

    def get_docs_count(self):
        return self.documents.count()
    

class UserDocument(models.Model):
    CREATED = 'CR'
    PURCHASED = 'PU'
    FINISHED = 'FI'
    EXPIRED = 'EX'

    STATUS_CHOICES = (
        (CREATED, 'Creado'),
        (PURCHASED, 'Comprado'),
        (FINISHED, 'Finalizado'),
        (EXPIRED, 'Caducado'),
    )

    user = models.ForeignKey(   
        User,
        verbose_name='Usuario',
        null=True,
        on_delete=models.SET_NULL
    )
    document = models.ForeignKey(
        Document,
        verbose_name='Documento',
        null=True,
        on_delete=models.SET_NULL
    )
    answers = JSONField(
        'Respuestas',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PURCHASED
    )
    identifier = models.UUIDField(
        default=uuid.uuid4, 
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    html_file = models.FileField(
        null=True,
        blank=True,
        editable=False,
        upload_to='documents'
    )
    pdf_file = models.FileField(
        null=True,
        blank=True,
        editable=False,
        upload_to='pdfs',
        max_length=500
    )
    word_file = models.FileField(
        null=True,
        blank=True,
        editable=False,
        upload_to='docxs',
        max_length=500
    )

    class Meta:
        verbose_name = 'Documento de usuario'
        verbose_name_plural = 'Documentos de usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.pk)
    
    def get_absolute_url(self):
        return reverse('webclient:user-document', kwargs={'identifier': self.identifier})
    
    def is_expired(self):
        diff = datetime.datetime.now() - self.created_at.replace(tzinfo=None)
        if diff.days > 10:
            return True
        return False


class Invoice(models.Model):
    """Guarda las facturas a cada usuario.
    """

    APPROVED = 'AP'
    PENDING  = 'PE'
    CANCEL  = 'CA'
    REJECTED  = 'RE'

    STATUS = (
        (APPROVED, 'Aprobada'),
        (PENDING,  'Pendiente'),
        (CANCEL,  'Cancelada'),
        (REJECTED,  'Rechazada'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )
    is_discharged = models.BooleanField('¿Está pago?', default=False)
    document = models.ForeignKey(
        Document,
        verbose_name='Documento',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    package = models.ForeignKey(
        DocumentBundle,
        verbose_name='Paquete',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    payment_date = models.DateTimeField(
        'Fecha de pago',
        auto_now_add=True,
        null=True,
        blank=True
    )
    payu_reference_code = models.CharField(
        'Referencia Pago payU',
        max_length=255,
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        'Estado del Pago',
        max_length=50,
        choices=STATUS,
        default=PENDING
    )

    class Meta:
        verbose_name = 'Factura'

    def __unicode__(self):
        return self.get_identifier()
    
    def get_identifier(self):
        return '{}{}'.format(
            self.pk,
            int(time.mktime(self.payment_date.timetuple()))
        )
    
    def get_purchased_element(self):
        if self.document:
            return self.document.name
        if self.package:
            return self.package.name
        return None