import uuid
from io import BytesIO

from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import render_to_string, get_template
from django.views import View

from docx import Document as DocX
from rest_framework import generics
from selenium import webdriver
from xhtml2pdf import pisa as pisa

from .models import (
    Document,
    DocumentField,
    DocumentSection,
    Document,
    Category
)
from .serializers import (
    DocumentFieldSerializer,
    DocumentSectionSerializer,
    DocumentSerializer,
    CategorySerializer
)
from .utils import add_document_scripts


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
        content = document.content + '<script \
            src="https://code.jquery.com/jquery-3.3.1.slim.min.js" \
            integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" \
            crossorigin="anonymous" type="text/javascript"></script> \
            <script type="text/javascript" src="https://unpkg.com/jspdf@latest/dist/jspdf.min.js"></script> \
            <script type="text/javascript" src="/static/js/pdfRender.js"></script>'
        template = Template(content)
        template = template.render(Context(request.POST)).encode('ascii', 'xmlcharrefreplace')

        return HttpResponse(template)
        if request.POST.get('pdf', None):
            pdf = pisa.pisaDocument(innerHTML)

            if not pdf.err:
                response = HttpResponse(pdf, content_type='application/pdf')
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


class DocumentList(generics.ListAPIView):
    """Api para obtener la lista de documentos de una categoría
    """

    serializer_class = DocumentSerializer

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        categories = category.get_descendants(include_self=True)
        return Document.objects.filter(category__in=categories).order_by('order')


class CategoryRootList(generics.ListAPIView):
    """Api para listar las categorías padre
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent=None)


class CategoryChildrenList(generics.ListAPIView):
    """Api para listar las categorías hijas de un padre
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Category.objects.filter(parent=category)


def category(request, path, instance):
    # This is an example view.
    # As you can see, this view receives additional arg - instance.

    if instance:
        categories = instance.get_descendants(include_self=True)
        documents = Document.objects.filter(category__in=categories).order_by('order')
    else:
        documents = Document.objects.all().order_by('order')

    return render(
        request,
        'webclient/documents.html',
        {
            'category': instance,
            'children': instance.get_children() if instance else Category.objects.root_nodes(),
            'documents': documents
        }
    )
