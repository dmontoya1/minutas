from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.views import View

from .models import Document
from .utils import render_to_pdf


class ProcessDocumentView(View):

    def post(self, request, *args, **kwargs):
        document = Document.objects.get(id=request.POST['document'])
        template = Template(document.content)
        template = template.render(Context(request.POST))
        format = request.POST['submit']
        response = HttpResponse(content_type='application/' + format)
        response['Content-Disposition'] = 'attachment; filename="PDF.{format}"'.format(format=format)
        return response