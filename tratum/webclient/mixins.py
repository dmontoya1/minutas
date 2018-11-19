# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views.generic import TemplateView

from tratum.users.models import LogTerms


class TermsAndConditions(TemplateView):
    """Clase para validar si el usuario ya tiene aceptados los
    términos y condiciones
    """

    def get(self, request, *args, **kwargs):

        user = request.user
        if not user.is_authenticated or user.is_superuser:
            return super(TermsAndConditions, self).get(request, *args, **kwargs)
        else:
            if LogTerms.objects.filter(user=user).exists():
                context = super(TermsAndConditions, self).get_context_data()
                return self.render_to_response(context)
            else:
                return redirect('/validate-terms/')
