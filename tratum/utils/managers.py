from django.db import models
from django.utils import timezone


class SoftDeletionQuerySet(models.QuerySet):
    """Queryset personalizado para agregar funcionalidades de borrado lógico a los modelos.
    """

    def delete(self):
        """Método para ejecutar un borrado lógico en el modelo"""

        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """Método para ejecutar un borrado físico en el modelo"""

        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        """Método para filtrar los objetos que lógicamente estén en la table"""

        return self.filter(deleted_at=None)

    def dead(self):
        """Método para filtrar los objetos que fueron lógicamente borrados"""

        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Manager personalizado para agregar funcionalidades de borrado lógico a los modelos.
    """

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()