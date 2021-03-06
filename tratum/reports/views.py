from io import BytesIO
import json

from django.http import HttpResponse

from django.template.loader import get_template
from django.views.generic.base import View

from xhtml2pdf import pisa

from .resources import (
    DocumentResource,
    CategoryResource,
    DocumentBundleResource,
    InvoiceResource
)


class DocumentExport(View):

    def post(self, request, *args, **kwargs):
        resource = DocumentResource()
        dataset = resource.export()
        if request.POST.get('CSV', None):
            export_type = dataset.csv
            content_type = 'text/csv'
            format = 'csv'
        elif request.POST.get('XLS', None):
            export_type = dataset.xls
            content_type = 'application/vnd.ms-excel'
            format = 'xls'
        elif request.POST.get('PDF', None):
            template_path = 'admin/document_reports/pdf_skeleton.html'

            context = {
                'summary': json.loads(dataset.json)
            }

            template = get_template(template_path)
            html = template.render(context)

            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse('Errors')

        response = HttpResponse(export_type, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="report.{}"'.format(format)
        return response


class CategoryExport(View):

    def post(self, request, *args, **kwargs):
        resource = CategoryResource()
        dataset = resource.export()
        if request.POST.get('CSV', None):
            export_type = dataset.csv
            content_type = 'text/csv'
            format = 'csv'
        elif request.POST.get('XLS', None):
            export_type = dataset.xls
            content_type = 'application/vnd.ms-excel'
            format = 'xls'
        elif request.POST.get('PDF', None):
            template_path = 'admin/category_reports/pdf_skeleton.html'

            context = {
                'summary': json.loads(dataset.json)
            }

            template = get_template(template_path)
            html = template.render(context)

            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse('Errors')

        response = HttpResponse(export_type, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="report.{}"'.format(format)
        return response


class DocumentBundleExport(View):

    def post(self, request, *args, **kwargs):
        resource = DocumentBundleResource()
        dataset = resource.export()
        if request.POST.get('CSV', None):
            export_type = dataset.csv
            content_type = 'text/csv'
            format = 'csv'
        elif request.POST.get('XLS', None):
            export_type = dataset.xls
            content_type = 'application/vnd.ms-excel'
            format = 'xls'
        elif request.POST.get('PDF', None):
            template_path = 'admin/bundle_reports/pdf_skeleton.html'

            context = {
                'summary': json.loads(dataset.json)
            }

            template = get_template(template_path)
            html = template.render(context)

            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse('Errors')

        response = HttpResponse(export_type, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="report.{}"'.format(format)
        return response


class InvoiceExport(View):

    def post(self, request, *args, **kwargs):
        resource = InvoiceResource()
        dataset = resource.export()
        if request.POST.get('CSV', None):
            export_type = dataset.csv
            content_type = 'text/csv'
            format = 'csv'
        elif request.POST.get('XLS', None):
            export_type = dataset.xls
            content_type = 'application/vnd.ms-excel'
            format = 'xls'
        elif request.POST.get('PDF', None):
            template_path = 'admin/user_reports/pdf_skeleton.html'

            context = {
                'summary': json.loads(dataset.json)
            }

            template = get_template(template_path)
            html = template.render(context)

            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), dest=result)
            if not pdf.err:
                return HttpResponse(result.getvalue(), content_type='application/pdf')
            else:
                return HttpResponse('Errors')

        response = HttpResponse(export_type, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="report.{}"'.format(format)
        return response
