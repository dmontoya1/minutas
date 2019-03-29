from tratum.document_manager.models import Document, Category
from tratum.store.models import DocumentBundle, Invoice


class DocumentSaleSummary(Document):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de venta de documentos'
        verbose_name_plural = 'Reportes de venta de documentos'


class UserDocumentsSummary(Invoice):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de compras de documentos de clientes'
        verbose_name_plural = 'Reportes de compras de documentos de clientes'


class CategorySaleSummary(Category):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de ventas documentos por categoría'
        verbose_name_plural = 'Reportes de ventas documentos por categoría'


class BundleSaleSummary(DocumentBundle):
    class Meta:
        proxy = True
        verbose_name = 'Reporte de ventas de paquetes'
        verbose_name_plural = 'Reportes de ventas de paquetes'

