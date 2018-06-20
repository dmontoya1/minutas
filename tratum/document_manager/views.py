import uuid
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import render_to_string
from django.views import View

from docx import Document as DocX
from rest_framework import generics
from xhtml2pdf import pisa as pisa

from .models import (
    Document,
    DocumentField,
    DocumentSection
)
from .serializers import (
    DocumentFieldSerializer,
    DocumentSectionSerializer
)


class DocumentFieldList(generics.ListAPIView):
    serializer_class = DocumentFieldSerializer

    def get_queryset(self):
        q = DocumentField.objects.all()
        if self.request.GET.get('document_id', None):
            q = q.filter(document__id=self.request.GET['document_id'])
        return q


class DocumentSectionList(generics.ListAPIView):
    serializer_class = DocumentSectionSerializer

    def get_queryset(self):
        q = DocumentSection.objects.all()
        if self.request.GET.get('document_id', None):
            q = q.filter(document__id=self.request.GET['document_id'])
        return q

class DocumentSectionFieldsList(DocumentFieldList):

    def get_queryset(self): 
        return DocumentField.objects.filter(section__slug=self.kwargs['slug'])
        

class DocumentSectionDetail(generics.RetrieveAPIView):
    serializer_class = DocumentSectionSerializer
    lookup_field = 'slug'

    def get_object(self):
        ins = DocumentSection()
        slug = ins.formated_to_raw_slug(self.kwargs['slug'])
        return DocumentSection.objects.get(slug=slug)
    

class ProcessDocumentView(View):

    def post(self, request, *args, **kwargs):
        document = Document.objects.get(id=request.POST['document'])
        content = document.content + '<script type="text/javascript" src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script> \
        <script type="text/javascript">$(document).ready(function(){$("p").css("color", "red")})</script>'
        template = Template(content)
        generated_document = template.render(Context(request.POST)).encode('ascii', 'xmlcharrefreplace')

        

        with open('{MEDIA}/documents/{name}.html'.format(
            MEDIA=settings.MEDIA_ROOT,
            name=uuid.uuid4()),'a+') as file:
            file.write(str(generated_document))

        return HttpResponse(generated_document)

        if request.POST.get('pdf', None):
            response = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(generated_document), response)

            if not pdf.err:
                response = HttpResponse(response.getvalue(), content_type='application/pdf')
                content_disposition = 'attachment; filename="{}.pdf"'.format(document.name)
                response['Content-Disposition'] = content_disposition
                return response
            else:
                return HttpResponse("Error Rendering PDF", status=400)
                
        elif request.POST.get('doc', None):
            doc = DocX()
            doc.add_paragraph('Contrato')

            response = HttpResponse(doc, content_type='application/docx')
            content_disposition = 'attachment; filename="{}.docx"'.format(document.name)
            response['Content-Disposition'] = content_disposition
            return response
