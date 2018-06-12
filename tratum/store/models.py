from django.db import models
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