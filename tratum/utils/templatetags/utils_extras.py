from django import template
from utils.models import SoftDeletionModelMixin


register = template.Library()

@register.filter(name="is_softdeletion_instance")
def is_softdeletion_instance(value):
    return isinstance(value, SoftDeletionModelMixin)
