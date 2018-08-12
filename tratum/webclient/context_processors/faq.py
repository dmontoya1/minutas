from business_info.models import FAQCategory


def faq_processor(request):    
    return {
        'faq_categories': FAQCategory.objects.all()
    }