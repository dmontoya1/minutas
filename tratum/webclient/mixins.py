# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from api.helpers import get_api_user
from users.models import LogTerms



class TermsAndConditions(TemplateView):
    """Clase para validar si el usuario ya tiene aceptados los
    términos y condiciones
    """

    def get(self, request, *args, **kwargs):

        user = request.user
        if not user.is_authenticated or user.is_superuser:
            return super(TermsAndConditions, self).get(request, *args, **kwargs)
        else:
            try:
                log = LogTerms.objects.get(user=user)
                context = super(TermsAndConditions, self).get_context_data() 
                return self.render_to_response(context)
            except LogTerms.DoesNotExist:
                return redirect('/validate-terms/')
        

