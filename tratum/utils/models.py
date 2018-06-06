from django.db import models
from django.utils import timezone
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
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModelMixin, self).delete()
