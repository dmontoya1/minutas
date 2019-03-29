from tratum.business_info.models import GlossaryCategory


def glossary_processor(request):
    return {
        'glossary_categories': GlossaryCategory.objects.all()
    }
