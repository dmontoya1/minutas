from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from document_manager.models import Document


class HomePageView(TemplateView):

    template_name = "webclient/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.all()
        return context


class DocumentDetailView(DetailView):

    model = Document


