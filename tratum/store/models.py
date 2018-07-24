from django.db import models
from django.contrib.auth.models import User
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Paquete de documento'   
        verbose_name_plural = 'Paquetes de documentos'


class UserDocument(models.Model):
    CREATED = 'CR'
    PURCHASED = 'PU'
    FINISHED = 'FI'

    STATUS_CHOICES = (
        (CREATED, 'Creado'),
        (PURCHASED, 'Comprado'),
        (FINISHED, 'Finalizado')
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
    answers = models.TextField(
        'Respuestas',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PURCHASED
    )

    class Meta:
        verbose_name = 'Documento de usuario'
        verbose_name_plural = 'Documentos de usuarios'

    def __str__(self):
        return self.pk 