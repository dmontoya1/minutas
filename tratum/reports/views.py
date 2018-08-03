from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from .resources import DocumentResource


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
        response = HttpResponse(export_type, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="report.{}"'.format(format)
        return response
