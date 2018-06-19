from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from .managers import SoftDeletionManager


class SoftDeletionModelMixin(models.Model):
    """Modelo abstracto para brindar borrado lógico a los modelos.

    Campos del modelo:
        deleted_at: Indica la fecha de borrado lógico del objecto. La nulabilidad de éste
        campo indica si el objeto está 'vivo' o no.
        objects: Manager personalizado
        all_objects: Manager personalizado para obtener todos los objetos, incluyendo 'vivos' y
        lógicamente borrados.
    """

    deleted_at = models.DateTimeField(blank=True, null=True)
    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Ejecuta un borrado lógico desde la instancia
        """

        self.deleted_at = timezone.now()
        self.save()

    def revive(self):
        """Habilita un objeto que esté lógicamente borrado
        """

        self.deleted_at = None
        self.save()
    

class SlugIdentifierMixin(models.Model):
    """Clase para brindar identificación por slug a los modelos.

    El Slug no entra a ser la llave primaria de la tabla, pero permite que el modelo
    tenga tanto un campo de Slug como un método que permita generarlo al guardar una 
    instancia del modelo y otro método para generar un slug para uso en variables de templates.

    Campos del modelo:
        slug: Campo con el slug del modelo

    """

    slug = models.SlugField(
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
    
    def _get_unique_slug(self):
        slug = self.name
        if hasattr(self, 'document'):
            if self.document:
                slug = slugify('{}-{}'.format(self.name, self.document.slug))
        if hasattr(self, 'section'):
            if self.section:
                slug = slugify('{}-{}'.format(self.name, self.section.slug))
        return slugify(slug)   
    
    def formated_slug(self):
        return str(self.slug).replace('-', '_')
    
    def formated_to_raw_slug(self, formated_slug):
        return formated_slug.replace('_', '-')
    