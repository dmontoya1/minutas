from import_export import resources
from import_export.fields import Field

from tratum.document_manager.models import (
    Document,
    Category
)
from tratum.store.models import (
    DocumentBundle,
    Invoice
)


class DocumentResource(resources.ModelResource):
    name = Field(attribute='name', column_name='nombre')
    category = Field(attribute='category', column_name='categoria')
    count = Field(column_name='cantidad')

    class Meta:
        model = Document
        fields = ('name', 'category')

    def dehydrate_count(self, document):
        return document.userdocument_set.all().count()


class CategoryResource(resources.ModelResource):
    name = Field(attribute='name', column_name='nombre')
    count = Field(column_name='cantidad')

    class Meta:
        model = Category
        fields = ('name',)

    def dehydrate_count(self, category):
        return category.get_purchased_docs_count()


class DocumentBundleResource(resources.ModelResource):
    name = Field(attribute='name', column_name='nombre')
    documents = Field(attribute='documents', column_name='documentos')
    count = Field(column_name='cantidad')

    class Meta:
        model = DocumentBundle
        fields = ('name', 'documents')

    def dehydrate_count(self, bundle):
        return bundle.invoice_set.all().count()


class InvoiceResource(resources.ModelResource):
    user = Field(attribute='user', column_name='usuario')
    payment_date = Field(attribute='payment_date', column_name='fecha')
    element = Field(column_name='elemento')

    class Meta:
        model = Invoice
        fields = ('user', 'payment_date')

    def dehydrate_element(self, invoice):
        return invoice.get_purchased_element()
