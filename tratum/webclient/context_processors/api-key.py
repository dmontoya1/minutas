from django.conf import settings


def api_key_processor(request):

    context = {
        'Api_Key': settings.API_KEY,
    }
    return context
