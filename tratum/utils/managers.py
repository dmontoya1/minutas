from django.db import models
from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    """Queryset personalizado para agregar funcionalidades de borrado lógico a los modelos.
    """

    def soft_delete(self):
        """Método para ejecutar un borrado lógico en el modelo"""
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def revive(self):
        """Método para habilitar/revivir los objetos seleccionados"""

        return super(SoftDeletionQuerySet, self).update(deleted_at=None)

    def alive(self):
        """Método para filtrar los objetos disponibles"""

        return self.filter(deleted_at=None)

    def dead(self):
        """Método para filtrar los objetos que fueron lógicamente borrados"""
       
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Manager personalizado para agregar funcionalidades de borrado lógico a los modelos.
    """

    def get_queryset(self):
        return SoftDeletionQuerySet(self.model)

    def soft_delete(self):
        return self.get_queryset().soft_delete()
    
    def alive(self):
        return self.get_queryset().alive()

    def revive(self):
        return self.get_queryset().revive()