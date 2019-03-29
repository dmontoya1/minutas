from tratum.document_manager.models import Category


def context_categories(request):
    return {
        'context_categories': Category.objects.filter(deleted_at=None, parent=None)
    }
