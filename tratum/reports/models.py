from django.db import models
from document_manager.models import Document

class DocumentSaleSummary(Document):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de venta de documentos'
        verbose_name_plural = 'Reporte de venta de documentos'

