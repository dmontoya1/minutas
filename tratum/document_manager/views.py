import json
import os
import platform 
import subprocess
import uuid


import pdfkit
import pypandoc


from io import BytesIO

from django.db.models import Q
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import EmailMultiAlternatives
from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render
from django.template import Template, Context, loader
from django.template.loader import render_to_string, get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from docx import Document as DocX
from rest_framework import generics
from selenium import webdriver
from xhtml2pdf import pisa as pisa

from store.models import DocumentBundle

from .models import (
    Document,
    DocumentField,
    DocumentSection,
    DocumentFieldOption,
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
from .utils import get_static_path


class DocumentFieldList(generics.ListAPIView):
    serializer_class = DocumentFieldSerializer

    def get_queryset(self):
        q = DocumentField.objects.all()
        if self.request.GET.get('document_id', None):
            q = q.filter(document__id=self.request.GET['document_id'])
        return q


class DocumentFieldDetail(generics.RetrieveAPIView):
    serializer_class = DocumentFieldSerializer
    lookup_field = 'slug'

    def get_object(self):
        ins = DocumentField()
        slug = ins.formated_to_raw_slug(self.kwargs['slug'])
        return DocumentField.objects.get(slug=slug)
        

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
        user_document = UserDocument.objects.get(id=request.POST['document'])
        pdf_file = open(user_document.pdf_path)


class SaveAnswersView(View):

    def post(self, request, *args, **kwargs):
        content = request.POST
        user_document = UserDocument.objects.get(identifier=request.POST['identifier'])
        user_document.answers = request.POST
        user_document.save()
        return HttpResponse(status=200)


class UserDocumentContentView(View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = {}
        obj = UserDocument.objects.get(identifier=body['identifier'])
        document_content = Template(obj.document.content)
        document_content = document_content.render(Context(obj.answers))
        content['document_content'] = document_content
        return JsonResponse(content) 


class LinkedFieldView(View):
    """Api para listar las preguntas linkeadas a una pregunta dinámica.
    Esta vista devuelve el HTML renderizado de los campos.
    """

    serializer_class = DocumentFieldSerializer

    def get(self, request, *args, **kwargs):
        q = DocumentFieldOption.objects.get(pk=kwargs['pk'])
        fields = q.linked_fields.all().order_by('-order')
        output = []
        for f in fields:
            template = loader.get_template('document_form/fields.html')
            render = template.render({'field': f})
            output.append(render)
        content = {}
        content['fields'] = output
        return JsonResponse(content)


class FinishDocumentView(View):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode('utf-8'))
        user_document = UserDocument.objects.get(identifier=body['identifier'])
        self.generate_html(request, user_document, body['content'])
        self.generate_doc(request, user_document)
        self.generate_pdf(request, user_document)
        self.update_status(user_document)
        self.send_email(request, user_document) 
        return HttpResponse(status=200)
    
    def update_status(self, user_document):
        user_document.status = UserDocument.FINISHED
        user_document.save()
    
    def generate_pdf(self, request, user_document):
        options = {
            'page-size': 'Letter',
            'margin-top': '1.20in',
            'margin-right': '1.20in',
            'margin-bottom': '1.20in',
            'margin-left': '1.00in',
            'encoding': "UTF-8",
            'footer-center': '[page]',
            'footer-spacing': '14',
            'footer-font-size': '9',
            'header-right': f'{user_document.document.name}',
            'header-spacing': '15',
            'header-font-size': '7',
            'javascript-delay': 300,
            'no-outline': None
        } 
        output_filename = f'{user_document.identifier}.pdf'
        html_file = user_document.html_file.read().decode('utf-8')
        file = pdfkit.PDFKit(html_file, "string", options=options).to_pdf()
        file = BytesIO(file)
        user_document.pdf_file.save(output_filename, file)
        file.close()
    
    def generate_doc(self, request, user_document):
        html_file = user_document.html_file.path
        name = os.path.basename(user_document.html_file.name.split('.')[0])
        output_filename = f'{name}.odt'
        media_root = settings.MEDIA_ROOT
        
        if platform.system() == 'Linux':
            subprocess.call(
                f'soffice --headless --convert-to odt {html_file} --outdir {media_root}/docxs/',
                shell=True
            )
        elif platform.system() == 'Darwin':
            subprocess.call(
                f'cd /Applications/LibreOffice.app/Contents/MacOS && \
                ./soffice --headless --convert-to odt {html_file} --outdir {media_root}/docxs/',
                shell=True
            )

        user_document.word_file = f'docxs/{output_filename}'
        user_document.save()

    def generate_html(self, request, user_document, TEMPORARY_HTML_FILE):

        def get_scripted_html(request, html_string):
            css_tag = lambda path: f'<link rel="stylesheet" type="text/css" href="{path}" />'
            script_tag = lambda path: f'<script src="{path}"></script>'
            django_temptag_tag = lambda path: '{{% load {path} %}}'.format(path=path)
            iterator = lambda tag, paths: [tag(path) for path in paths]
            css_paths = (
                get_static_path(
                    request.scheme,
                    request.get_host(),
                    static("css/pdf_formatter.css")
                ),
            )
            script_paths = (
                get_static_path(
                    request.scheme,
                    request.get_host(),
                    static("js/pdfRender.js")
                ),
            )
            django_temptag_paths = (
                'fieldformatter',
            )
            scripts = '\n'.join(iterator(script_tag, script_paths))
            css = '\n'.join(iterator(css_tag, css_paths))
            django_temptags = '\n'.join(iterator(django_temptag_tag, django_temptag_paths))
            escape = '\n'
            return f'{django_temptags} {escape} {css} {html_string} {escape} {scripts}'

        """ content = get_scripted_html(request, user_document.document.content)
        template = Template(content)
        template = template.render(Context(user_document.answers)).encode('ascii', 'xmlcharrefreplace') """

        file = ContentFile(TEMPORARY_HTML_FILE.encode('ascii', 'xmlcharrefreplace'))
        user_document.html_file.save(f'{user_document.identifier}.html', file)       
    
    def send_email(self, request, user_document):
        subject = f'Tu {user_document.document.name} de Tratum'
        context = {
            'title': subject,
            'username': user_document.user.get_full_name(),
            'content': 'Adjunto encontrarás el documento que generaste en Tratum.',
            'action_url': False
        }
        body = loader.get_template('email/base.html').render(context)
        kwargs = dict(
            to=[user_document.user.email],
            from_email='no-reply@tratum.co',
            subject=subject,
            body=body
        )
        message = EmailMultiAlternatives(**kwargs)
        message.content_subtype = 'html'
        message.attach_file(user_document.pdf_file.path)
        message.send()
        

class DocumentList(generics.ListAPIView):
    """Api para obtener la lista de documentos de una categoría
    """

    serializer_class = DocumentSerializer

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        categories = category.get_descendants(include_self=True)
        return Document.objects.filter(category__in=categories).order_by('order')


class MainDocumentList(generics.ListAPIView):
    """Api para obtener la lista de documentos con buscador
    """

    serializer_class = DocumentSerializer

    def get_queryset(self):
        q = self.request.GET.get('term', None)
        if q:
            return Document.objects.filter(name__contains=q)
        return Document.objects.filter(deleted_at=None)


class CategoryRootList(generics.ListAPIView):
    """Api para listar las categorías padre
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent=None, deleted_at=None)


class CategoryChildrenList(generics.ListAPIView):
    """Api para listar las categorías hijas de un padre
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return Category.objects.filter(parent=category, deleted_at=None)


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
                document_list = Document.objects.filter(Q(price=0) | Q(price=None, deleted_at=None), category__in=categories,).order_by('order')
            else:
                document_list = Document.objects.filter(Q(price=0) | Q(price=None), deleted_at=None).order_by('order')
        elif request.GET.get('pay'):
            if instance:
                categories = instance.get_descendants(include_self=True)
                document_list = Document.objects.filter(category__in=categories, price__gt=0, deleted_at=None).order_by('order')
            else:
                document_list = Document.objects.filter(price__gt=0, deleted_at=None).order_by('order')
        else:
            package_list = DocumentBundle.objects.all().order_by('order')

    else:
        if instance:
            categories = instance.get_descendants(include_self=True)
            document_list = Document.objects.filter(category__in=categories, deleted_at=None).order_by('order')
        else:
            if q:
                document_list = Document.objects.filter(
                    Q(name__icontains=q) | Q(category__name__icontains=q),
                    deleted_at=None
                ).order_by('order')
            else:
                document_list = Document.objects.filter(deleted_at=None).order_by('order')


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

class ChangeAdminOrder(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ChangeAdminOrder, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        field = request.POST['pk']
        order = request.POST['order']
        field = DocumentField.objects.get(pk=field)
        field.order = order
        field.save()
        return HttpResponse(status=200)