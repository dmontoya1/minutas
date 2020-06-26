from django.shortcuts import redirect

from tratum.users.models import LogTerms


class TermsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        terms_path = '/validate-terms/'
        path = request.path
        if path != terms_path:
            if request.user.is_authenticated and not request.user.is_staff:
                if not LogTerms.objects.filter(user=request.user).exists():
                    return redirect(terms_path)
        return response
