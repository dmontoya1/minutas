from tratum.business_info.models import SiteConfig, SliderItem, MainCategory
from tratum.store.models import (
    DocumentBundle
)


def business_info_processor(request):
    context = {}
    site_config = SiteConfig.objects.last()
    if site_config:
        context['bussiness_info'] = site_config
        context['landing_contract_info'] = site_config.landing_contract_info
        context['landing_bundles_info'] = site_config.landing_bundles_info
    context['context_bundles'] = DocumentBundle.objects.alive().filter(show_on_landing=True)
    context['context_slides'] = SliderItem.objects.all()
    context['context_bundle_count'] = DocumentBundle.objects.alive().count()
    context['main_categories'] = MainCategory.objects.all()
    return context
