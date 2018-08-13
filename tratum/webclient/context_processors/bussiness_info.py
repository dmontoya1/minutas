from business_info.models import SiteConfig


def bussiness_info_processor(request):    
    return {
        'bussiness_info': SiteConfig.objects.last()
    }