from import_export import resources
from import_export.fields import Field

from document_manager.models import Document


class DocumentResource(resources.ModelResource):
    name = Field(attribute='name', column_name='nombre')
    category = Field(attribute='category', column_name='categoria')
    count = Field(column_name='cantidad')
    
    class Meta:
        model = Document
        fields = ('name', 'category',)
    
    def dehydrate_count(self, document):
        return document.userdocument_set.all().count()
    
   
        