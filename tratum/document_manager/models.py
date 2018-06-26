# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os 
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from utils.models import SoftDeletionModelMixin, SlugIdentifierMixin


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


class Document(SoftDeletionModelMixin, SlugIdentifierMixin):
    """Guarda las documentos.

    Campos del modelo:
        name: Nombre del documento
        category: Categoría a la que pertenece el documento
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
    template_path = models.TextField(
        null=True,
        blank=True
    )
    formated = models.BooleanField(
        default=False
    )
    content = RichTextField(
        'Contenido',
        null=True, 
        blank=True
    )
 
    class Meta:
        verbose_name = 'Documento'

    def __str__(self):
        return self.name     
    
    def save(self):
        path = os.path.join(settings.BASE_DIR, "document_manager/templates/document_manager/dynamic_documents_templates")
        html_template = open('{}/{}.html'.format(path, uuid.uuid4()), 'w+')
        html_template.write(self.content)
        html_template.close()
        self.template_path = html_template.name
        SlugIdentifierMixin.save(self)

    def get_absolute_url(self):
        return reverse('document', kwargs={'slug': self.slug})

    def query_component(self, slug: str):
        slug = self.formated_to_raw_slug(slug)
        try:
            component = self.documentfield_set.get(slug=slug)
        except:
            try:
                component = self.documentsection_set.get(slug=slug)
            except:
                component = None
        return component

    def get_components(self, type_: str):
        c = str(self.content)        
        fields = []
        sections = []
        result = []
        if type_ == 'fields':
            result = fields
            ex = r'{{(.*?)}}'
        elif type_ == 'sections':
            result = sections
            ex = r'{% if (.*?) %}'
        raw_fields = re.findall(ex, c)
        for f in raw_fields:
            component = self.query_component(f)
            if component is not None:
                if isinstance(component, DocumentField) and component not in fields:
                    fields.append(component)
                elif isinstance(component, DocumentSection) and component not in sections:
                    sections.append(component)
        
        return result

    def get_fields(self):
        return self.get_components('fields')
    
    def get_sections(self):
        return self.get_components('sections') 


class DocumentSection(SlugIdentifierMixin):
    """Guarda las secciones opcionales/claúsulas de un documento

    Campos del modelo:
        name: Nombre del campo
        content: Contenido enriquecido 
        document: Lláve foránea al documento

    """

    name = models.CharField(max_length=255)
    content = RichTextField(
        'Contenido',
        null=True,
        blank=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    
    class Meta:
        unique_together = ('name', 'document')

    def __str__(self):
        return self.name 


class DocumentField(SlugIdentifierMixin):
    """Guarda los campos de los documentos y las secciones

    Campos del modelo:
        name: Nombre del campo
        help_text: Texto de ayuda para el usuario final
        youtube_help_video_link: URL del video de Youtube para el video de ayuda 
        del usuario final
        document: Lláve foránea al documento
        
    """ 

    NUMBER = 'NU'
    TEXT = 'TX'
    DATE = 'DT'
    SELECT = 'SE'
    LIST = 'LI'
    GROUP = 'GP'

    FIELD_TYPE = (
        (NUMBER, 'Numérico'),
        (TEXT, 'Texto abierto'),
        (DATE, 'Fecha'),
        (SELECT, 'Opciones de única respuesta'),
        (LIST, 'Listado'),
        (GROUP, 'Agrupación de campos')
    )

    name = models.CharField(
        'Nombre',
        max_length=255
    )
    help_text = models.TextField(
        'Texto de ayuda',
        blank=True,
        null=True
    )
    youtube_help_video_link = models.URLField(
        'Link de Youtube del video de ayuda',
        blank=True,
        null=True
    )
    field_type = models.CharField(
        'Tipo de campo',
        max_length=2,
        default=TEXT,
        choices=FIELD_TYPE
    ) 
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Documento'
    )
    section = models.ForeignKey(
        DocumentSection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Sección'
    )
    
    class Meta:
        unique_together = ('name', 'document')
        
    def __str__(self):
        return self.name   

    def clean(self):
        if self.document and self.section:
            raise ValidationError('Tu campo no puede pertenecer a un documento y a una sección simultáneamente')
        if not self.document and not self.section:
            raise ValidationError('Selecciona un documento o una sección para éste campo')

