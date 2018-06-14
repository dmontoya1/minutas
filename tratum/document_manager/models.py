import re
import uuid

from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from utils.models import SoftDeletionModelMixin


class Category(MPTTModel, SoftDeletionModelMixin):
    """Guarda las categorías de documentos.

    Campos del modelo:
        name: Nombre de la categoría
        parent: Para la estructura por árboles de la librería MPTT, indica el nodo 
        padre de la categoría si ésta lo requiere, de lo contrario (si el campo es nulo),
        indicará que la categoría es una categoría principal.
    """

    name = models.CharField(
        'Nombre',
        max_length=50,
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Categoría padre'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoría'

    class MPTTMeta:
        order_insertion_by = ['name']


class Document(SoftDeletionModelMixin):
    """Guarda las documentos.

    Campos del modelo:
        name: Nombre del documento
        category: Categoría a la que pertenece el documento
        slug: Identificador único para URLs y reversing
        content: Contenido enriquecido con la estructura dinámica del documento

    """

    name = models.CharField(
        'Nombre',
        max_length=255,
        unique=True
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Categoría'
    )
    slug = models.SlugField(
        null=True,
        blank=True
    )
    content = RichTextField('Contenido')

    class Meta:
        verbose_name = 'Documento'

    def __str__(self):
        self.get_sections()
        return self.name    

    def save(self, *args, **kwargs):
        self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = '{}-{}'.format(slug, self.id)
        return unique_slug    
    
    def get_absolute_url(self):
        return reverse('document', kwargs={'slug': self.slug})

    def query_component(self, key):
        try:
            component = self.documentfield_set.get(key=key)
        except:
            try:
                component = self.documentsection_set.get(key=key)
            except:
                component = None
        return component

    def get_components(self, type_):
        c = str(self.content)        
        fields = []
        sections = []
        ex = r'{{(.*?)}}'
        query = lambda f: self.query_component(key=f)
        raw_fields = re.findall(ex, c)
        for f in raw_fields:
            component = query(f)
            if component is not None:
                if isinstance(component, DocumentField):
                    fields.append(component)
                elif isinstance(component, DocumentSection):
                    sections.append(component)
        if type_ == 'fields':
            result = fields
        elif type_ == 'sections':
            result = sections
        return result

    def get_fields(self):
        return self.get_components('fields')
    
    def get_sections(self):
        return self.get_components('sections')


class DocumentField(models.Model):
    """Guarda los campos de los documentos

    Campos del modelo:
        name: Nombre del campo
        help_text: Texto de ayuda para el usuario final
        youtube_help_video_link: URL del video de Youtube para el video de ayuda 
        del usuario final
        document: Lláve foránea al documento

    """

    name = models.CharField(max_length=255)
    help_text = models.TextField(
        blank=True,
        null=True
    )
    youtube_help_video_link = models.URLField(
        blank=True,
        null=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    def __str__(self):
        return self.name    
    
    def clean_uuid(self):
        return str(self.key).replace('-', '')


class DocumentSection(models.Model):
    """Guarda las secciones opcionales/claúsulas de un documento

    Campos del modelo:
        name: Nombre del campo
        content: Contenido enriquecido 
        document: Lláve foránea al documento

    """

    name = models.CharField(max_length=255)
    content = RichTextField('Contenido')
    key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.name   
    
    def clean_uuid(self):
        return str(self.key).replace('-', '')

    