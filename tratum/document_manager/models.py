import re

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
        visible: Indica si la categoría y sus documentos y subcategorías relacionadas se verán o no
        en la tienda de documentos
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
    visible = models.BooleanField(
        '¿Disponible en la plataforma?',
        default=True
    )

    class Meta:
        verbose_name = 'Categoría'

    class MPTTMeta:
        order_insertion_by = ['name']


class Document(models.Model):
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
        self.get_fields()
        return self.name    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = '{}-{}'.format(slug, self.pk)
        return unique_slug    
    
    def get_absolute_url(self):
        return reverse('document', kwargs={'slug': self.slug})

    def get_fields(self):
        c = str(self.content)        
        fields = []
        raw_fields = re.findall(r'{{(.*?)}}', c)
        for f in raw_fields:
            try:
                name, type = f.split('*')
            except ValueError:
                name = f
                type = False
            field = {}
            field['raw_name'] = name
            field['name'] = name.capitalize().replace('_', ' ')
            field['type'] = type 
            fields.append(field) 
        print(fields)
        return fields