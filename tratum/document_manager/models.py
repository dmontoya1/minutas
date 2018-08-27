# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import os 
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

from utils.models import SoftDeletionModelMixin, SlugIdentifierMixin


class Category(MPTTModel, SoftDeletionModelMixin, SlugIdentifierMixin):
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
        unique_together = ('slug', 'parent')

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def clean(self):
        if self.parent:
            if self.parent.get_ancestors().count() == 3:
                raise ValidationError('Las categorías sólo pueden tener hasta 4 niveles de profundidad')
    
    def get_absolute_url(self):
        # return reverse('webclient:category-documents', kwargs={'slug': self.slug})
        return reverse('webclient:category_documents', kwargs={'path': self.get_path()})

    def get_purchased_docs_count(self):
        docs = self.document_set.all()
        i = 0
        for d in docs:
            i = i + d.userdocument_set.all().count()
        return i


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
    short_description = models.CharField(
        'Descripción corta',
        blank=True,
        null=True,
        max_length=120,
        help_text="Cantidad máxima de caracteres: 120"
    )
    long_description = models.TextField(
        'Descripción larga',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Categoría',      
    )
    template_path = models.TextField(
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(
        'Precio',
        null=True,
        blank=True
    )
    order = models.PositiveSmallIntegerField(
        'Orden',
        null=True,
        blank=True,
        unique=True
    )
    content = RichTextField(
        'Contenido',
        null=True, 
        blank=True
    )
    video_url = models.URLField(
        'URL del video explicativo',
        blank=True,
        null=True
    )
 
    class Meta:
        verbose_name = 'Documento'
        unique_together = ('category', 'order')

    def __str__(self):
        return self.name     

    def get_absolute_url(self):
        return reverse('webclient:document', kwargs={'slug': self.slug})

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
            f = f.split('|')[0]
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
    display_name = models.CharField(
        'Texto a mostrar',
        max_length=255,
        null=True,
        blank=True,
        help_text='Corresponde a la pregunta textual que verán los usuarios'
    )
    content = RichTextField(
        'Contenido',
        null=True,
        blank=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
    )
    help_text = models.TextField(
        'Texto de ayuda',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        unique_together = ('name', 'document')

    def __str__(self):
        return self.name 
    
    def get_fields(self):
        return self.documentfield_set.all().exclude(
            Q(field_group__isnull=False) & ~Q(field_type=DocumentField.GROUP) 
        )


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
    NATURAL_DATE = 'ND'
    SELECT = 'SE'
    SELECT_MULTIPLE = 'SM'
    LIST = 'LI'
    GROUP = 'GP'

    FIELD_TYPE = (
        (NUMBER, 'Numérico'),
        (TEXT, 'Texto abierto'),
        (DATE, 'Fecha'),
        (NATURAL_DATE, 'Fecha natural'),
        (SELECT, 'Opciones de única respuesta'),
        (SELECT_MULTIPLE, 'Opciones agrupadas'),
        (LIST, 'Listado'),
        (GROUP, 'Agrupación de campos')
    )

    name = models.CharField(
        'Nombre',
        max_length=255
    )
    display_name = models.CharField(
        'Texto a mostrar',
        max_length=255,
        null=True,
        blank=True,
        help_text='Corresponde a la pregunta textual que verán los usuarios'
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
    field_group = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Campos del grupo'
    )
    field_group_verbose_name = models.CharField(
        'Nombre singular de la agrupación',
        help_text='Corresponde a la palabra en singular que indica la referencia de la agrupación\
            Ej: Socio, Empresa, Actividad',
        null=True,
        blank=True,
        max_length=255
    )
    group_expression = models.TextField(
        'Expresión regular de la agrupación',
        help_text='Indica la expresión final de cada campo del grupo mediante el lenguaje de formateo',
        null=True,
        blank=True
    )
    group_order = models.PositiveIntegerField(
        'Orden de campo en el grupo',
        help_text='Indica el orden de aparición del campo en el formulario (Sólo aplica para grupos)',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Campo'
        unique_together = ('name', 'document')
        
    def __str__(self):
        return self.name   

    def clean(self):
        if self.document and self.section:
            raise ValidationError('Tu campo no puede pertenecer a un documento y a una sección simultáneamente')
        if not self.document and not self.section:
            raise ValidationError('Selecciona un documento o una sección para éste campo')
    
    def is_text_input(self):
        return self.field_type in (self.TEXT, self.DATE, self.NUMBER, self.NATURAL_DATE)
    
    def is_date_input(self):
        return self.field_type in (self.DATE, self.NATURAL_DATE)

    def get_html_input_type(self):
        if self.field_type == self.TEXT or self.field_type == self.LIST:
            return 'text'
        elif self.field_type == self.DATE or self.field_type == self.NATURAL_DATE:
            return 'date'
        elif self.field_type == self.NUMBER:
            return 'number'
    
    def get_ordered_group_fields(self):
        return self.field_group.all().order_by('group_order')


class DocumentFieldOption(models.Model):
    name = models.TextField(
        'Nombre',
        null=True,
        blank=True
    )
    field = models.ForeignKey(
        DocumentField,
        on_delete=models.CASCADE,
        verbose_name='Campo'
    )

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'

    def __str__(self):
        return self.name 
    
    def clean(self):
        if self.field.is_text_input():
            raise ValidationError('El campo debe ser tipo "Opciones de única respuesta" para agregarle opciones')




