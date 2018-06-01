from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.views import View

from .models import Document
from .utils import render_to_pdf


class ProcessDocumentView(View):

    def post(self, request, *args, **kwargs):
        for f in request.POST.items():
            print(str(f).encode())
        document = Document.objects.get(id=request.POST['document'])
        template = Template(document.content)
        template = template.render(Context(request.POST))
        return HttpResponse(template)