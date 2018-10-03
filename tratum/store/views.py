# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time

from datetime import datetime

from raven.contrib.django.raven_compat.models import client
from rest_framework import generics, status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView

from document_manager.models import Document

from .models import DocumentBundle, UserDocument, Invoice
from .serializers import DocumentBundleSerializer, UserDocumentSerializer



class DocumentBundleList(generics.ListAPIView):
    queryset = DocumentBundle.objects.alive()
    serializer_class = DocumentBundleSerializer


class CreateUserDocument(View):
    """CLASE DE PRUEBA PARA EMULAR COMPRA
    """
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('webclient:home'))
        document = UserDocument(
            user=request.user,
            document=Document.objects.get(pk=request.GET['document_id']) 
        )
        document.save()
        return HttpResponseRedirect(reverse('webclient:user-document', kwargs={'identifier': document.identifier}))


class UserDocumentDetailView(generics.RetrieveAPIView):
    lookup_field = 'identifier'
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer


class Checkout(TemplateView):
    """Vista para ver el formulario de seleccionar plan y moneda
    que se va a comprar
    """
    template_name = 'store/checkout.html'

    def post(self, request, *args, **kwargs):

        tax = 0
        taxReturnBase = 0
        description = "Compra realizada desde Tratum"


        if settings.DEBUG:
            test = 1
            accountId = 512321
            apiKey = '4Vj8eK4rloUd272L48hsrarnUA'
            merchantId = 508029
            url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu"
            host = 'http://tratum.apptitud.com.co'
        else:
            test = 0
            accountId = 746396
            apiKey = 'vIB29Yn5GW0XVv6qVYBV1e92T1'
            merchantId = 740818
            url = "https://checkout.payulatam.com/ppp-web-gateway-payu"
            host = 'http://tratum.co'

        currency = 'COP'

        try:
            try:
                documents = Document.objects.filter(pk=request.POST['doc_id'])
                doc_type = 'doc'
                ref = 'DO'
                id_ref = documents.first().pk
            except MultiValueDictKeyError:
                package = DocumentBundle.objects.get(pk=request.POST['pack_id'])
                documents = package.documents.all()
                doc_type = package.name
                ref = 'PA'
                id_ref = package.pk
        except Exception as e:
            print (e)        

        amount = 0
        for doc in documents:
            if doc.price:
                amount = amount + int(doc.price)
        referenceCode = '{}_{}_{}_{}'.format(ref, request.user.pk, id_ref, int(time.mktime(datetime.now().timetuple())))
        responseUrl = '{}/store/confirmation/'.format(host)
        confirmationUrl = '{}/store/confirmation/'.format(host)
        signature = '{}~{}~{}~{}~{}'.format(apiKey, merchantId,\
                    referenceCode, amount, currency)
        signature = signature.encode('utf-8')
        signature = hashlib.md5(signature).hexdigest()

        ctx = {
            'type': doc_type,
            'documents': documents,
            'merchantId' : merchantId,
            'description': description,
            'referenceCode': referenceCode,
            'amount' : amount,
            'tax' : tax,
            'taxReturnBase': taxReturnBase,
            'currency' : currency,
            'signature' : signature,
            'test' : test,
            'buyerEmail' : request.user.email,
            'responseUrl' : responseUrl,
            'accountId' : accountId,
            'confirmationUrl' : confirmationUrl,
            'url' : url,
        }

        return render(
            request,
            'store/checkout.html',
            ctx
        )

    @classmethod
    @method_decorator(csrf_exempt)
    def confirmation(self, request):
        if settings.DEBUG:
            apiKey     = '4Vj8eK4rloUd272L48hsrarnUA'
        else:
            apiKey     = 'vIB29Yn5GW0XVv6qVYBV1e92T1'
        
        if request.method == "POST":
            merchand_id = request.POST['merchant_id']
            reference_sale = request.POST['reference_sale']
            reference_pol = request.POST['reference_pol']
            state_pol = request.POST['state_pol']
            value  = request.POST['value']
            currency = request.POST['currency']
            sign = request.POST['sign']
            date = request.POST['date']

            value_str = str(value)

            value_antes, value_despues = value_str.split(".")
            value_despues = list(value_despues)
            if value_despues[1] == '0':
                value= round(float(value),1)
            signature = '{}~{}~{}~{}~{}~{}'.format(apiKey, merchand_id,reference_sale, value, currency,state_pol)
            signature = signature.encode('utf-8')
            signature = hashlib.md5(signature).hexdigest()

            reference = reference_sale.split('_')
            ref = reference[0]
            user_id = reference[1]
            ref_id = reference[2]


            if signature == sign:
                user = User.objects.get(pk=user_id)
                invoice = Invoice(
                    user = user,
                )
                invoice.save()
                if ref == 'DO':
                    documents = Document.objects.filter(pk=ref_id)
                    invoice.document = documents.first()
                else:
                    package = DocumentBundle.objects.get(pk=ref_id)
                    documents = package.documents.all()
                    invoice.package = package
                invoice.save()

                #Aprobada
                if state_pol == '4':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference
                    invoice.payment_status = Invoice.APPROVED
                    invoice.save()

                    for doc in documents:
                        d = UserDocument(
                            user=user,
                            document=doc,
                            status=UserDocument.CREATED,
                        )
                        d.save()

                    return HttpResponse(status=200)
                #Declinada
                elif state_pol == '6':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference
                    invoice.payment_status = Invoice.REJECTED
                    invoice.save()
                    return HttpResponse(status=200)
                #Error
                elif state_pol == '104':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference
                    invoice.payment_status = Invoice.CANCEL
                    invoice.save()
                    return HttpResponse(status=200)
                #Expirada
                elif state_pol == '5':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference
                    invoice.payment_status = Invoice.CANCEL
                    invoice.save()
                    return HttpResponse(status=200)
                #Pendiente
                elif state_pol == '7':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference
                    invoice.payment_status = Invoice.PENDING
                    invoice.save()
                    return HttpResponse(status=200)
                #ninguno de los state_pol
                else:
                    return HttpResponse(status=500)
            else:
                return HttpResponse(status=500)
        
        elif request.method == "GET":
            merchand_id = request.GET.get('merchantId','')
            referenceCode = request.GET.get('referenceCode','')
            transactionState = request.GET.get('transactionState','')
            value = request.GET.get('TX_VALUE','')
            currency = request.GET.get('currency','')
            signature_get = request.GET.get('signature','')
            reference_pol = request.GET.get('reference_pol')
            polPaymentMethodType = request.GET.get('polPaymentMethodType')

            value_str = str(value)

            value_antes, value_despues = value_str.split(".")

            value_despues= list(value_despues)
            
            primer_parametro_despues = int(value_despues[0])
            segundo_parametro_despues = int(value_despues[1])

            if primer_parametro_despues % 2 == 0:
                if segundo_parametro_despues == 5:
                    value_1= value-0.1
                    value = round(value_1,1)
                else:
                    value = round(float(value),1)
            elif primer_parametro_despues % 2 != 0: 
                if segundo_parametro_despues == 5:
                    value_1= value+0.1
                    value = round(float(value_1),1)
                else:
                    value = round(float(value),1)
            
            signature = '{}~{}~{}~{}~{}~{}'.format(apiKey, merchand_id,referenceCode, value, currency,transactionState)
            signature = signature.encode('utf-8')
            signature = hashlib.md5(signature).hexdigest()

            reference = referenceCode.split('_')
            ref = reference[0]
            user_id = reference[1]
            ref_id = reference[2]

            identifier = None
            if ref == 'DO':
                try:
                    document = Document.objects.get(pk=ref_id)
                    user = get_user_model().objects.get(pk=user_id)
                    user_doc = UserDocument.objects.filter(user=user, document=document).last()
                    identifier = user_doc.identifier
                except Exception as e:
                    client.captureException(e)
                    pass

            if signature == signature_get:  

                return render(
                    request,
                    'store/payment-resumen.html',
                    {
                        'merchand_id':merchand_id, 
                        'referenceCode':referenceCode,
                        'transactionState':transactionState,
                        'value':value,
                        'currency':currency,
                        'id_compra':referenceCode,
                        'reference_pol': reference_pol,
                        'polPaymentMethodType': polPaymentMethodType,
                        'ref': ref,
                        'identifier': identifier,
                    }
                    
                ) 
        else:
            return HttpResponseNotAllowed("Método no permitido")
