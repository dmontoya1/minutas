import json
import uuid
from io import BytesIO

from django.db.models import Q
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import render_to_string, get_template
from django.views import View

from docx import Document as DocX
from rest_framework import generics
from selenium import webdriver
from xhtml2pdf import pisa as pisa

from store.models import DocumentBundle

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
from store.models import UserDocument
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


class SaveAnswersView(View):

    def post(self, request, *args, **kwargs):
        content = request.POST
        user_document = UserDocument.objects.get(identifier=request.POST['identifier'])
        user_document.answers = request.POST
        user_document.save()
        return HttpResponse(status=200)


class FinishDocumentView(View):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        user_document = UserDocument.objects.get(identifier=body['identifier'])
        user_document.status = UserDocument.FINISHED
        user_document.save()
        return HttpResponse(status=200)
        

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

    documents = None
    document_list = None
    packages = None
    package_list = None
    q = request.GET.get('q', None)

    if request.GET.get('free') is not None or request.GET.get('pay') is not None or request.GET.get('package') is not None:
        if request.GET.get('free'):
            if instance:
                categories = instance.get_descendants(include_self=True)
                document_list = Document.objects.filter(Q(price=0) | Q(price=None), category__in=categories,).order_by('order')
            else:
                document_list = Document.objects.filter(Q(price=0) | Q(price=None)).order_by('order')
        elif request.GET.get('pay'):
            if instance:
                categories = instance.get_descendants(include_self=True)
                document_list = Document.objects.filter(category__in=categories, price__gt=0).order_by('order')
            else:
                document_list = Document.objects.filter(price__gt=0).order_by('order')
        else:
            package_list = DocumentBundle.objects.all().order_by('order')

    else:
        if instance:
            categories = instance.get_descendants(include_self=True)
            document_list = Document.objects.filter(category__in=categories).order_by('order')
        else:
            if q:
                document_list = Document.objects.filter(
                    Q(name__icontains=q) | Q(category__name__icontains=q)
                ).order_by('order')
                print(document_list)
            else:
                document_list = Document.objects.all().order_by('order')


    if document_list:
        paginator = Paginator(document_list, 8)
        page = request.GET.get('page')
        documents = paginator.get_page(page)
    elif package_list:
        paginator = Paginator(package_list, 8)
        page = request.GET.get('page')
        packages = paginator.get_page(page)
    
    return render(
        request,
        'webclient/documents.html',
        {
            'category': instance,
            'children': instance.get_children() if instance else Category.objects.root_nodes(),
            'documents': documents,
            'packages': packages
        }
    )
