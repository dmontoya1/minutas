# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib
import time

from datetime import datetime

from rest_framework import generics, status

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView

from document_manager.models import Document

from .models import DocumentBundle, UserDocument
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
        return HttpResponseRedirect(reverse('webclient:user-documents'))


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
        description = "Compra realizada desde Clinket"

        if settings.DEBUG:
            test = 1
            accountId = 512321
            apiKey = '4Vj8eK4rloUd272L48hsrarnUA'
            merchantId = 508029
            url = "https://sandbox.checkout.payulatam.com/ppp-web-gateway-payu"
            host = 'http://clinket.apptitud.com.co'
        else:
            test = 0
            accountId = 730741
            apiKey = 'IXltfYxCYPA2efIuyqj3L8k3uG'
            merchantId = 725814
            url = "https://checkout.payulatam.com/ppp-web-gateway-payu"
            host = 'http://clinket.com'


        try:
            suscription = Subscription.objects.get(pk=request.POST['plan_id'])
        except Exception as e:
            print (e.message)
        
        recurrency = request.POST['recurrency']

        if recurrency == 'month':
            try:
                currency = request.POST['cop_month_'+str(request.POST['plan_id'])]
            except MultiValueDictKeyError:
                currency = request.POST['usd_month_'+str(request.POST['plan_id'])]
            
            if currency == 'COP':
                amount = suscription.cop_mo_price
            else:
                amount = suscription.usd_mo_price
        else:
            try:
                currency = request.POST['cop_year_'+str(request.POST['plan_id'])]
            except MultiValueDictKeyError:
                currency = request.POST['usd_year_'+str(request.POST['plan_id'])]
            
            if currency == 'COP':
                amount = suscription.cop_ye_price
            else:
                amount = suscription.usd_ye_price


        
        if suscription.staff_limit == 0:
            staff = _("Ilimitado")
        else:
            staff = suscription.staff_limit
        
        if suscription.appointments_limit == 0:
            appointments = _("Ilimitado")
        else:
            appointments = suscription.appointments_limit
        

        amount = int(amount)
        referenceCode = 'RE_{}_{}'.format(request.user.staff_profile.pk, int(time.mktime(datetime.now().timetuple())))
        responseUrl = '{}/es/payments/confirmation/'.format(host)
        confirmationUrl = '{}/es/payments/confirmation/'.format(host)
        signature = '{}~{}~{}~{}~{}'.format(apiKey, merchantId,\
                    referenceCode, amount, currency)
        signature = hashlib.md5(signature).hexdigest()

        ctx = {
            'name': suscription.name,
            'recurrency': recurrency,
            'appointments': appointments,
            'staff': staff,
            'report': suscription.has_enabled_reports,
            'customers_bd': suscription.has_customers_bd,
            'merchantId' : merchantId,
            'description': description,
            'referenceCode': referenceCode,
            'amount' : amount,
            'tax' : tax,
            'taxReturnBase': taxReturnBase,
            'currency' : currency,
            'signature' : signature,
            'test' : test,
            'buyerEmail' : request.user.username,
            'responseUrl' : responseUrl,
            'accountId' : accountId,
            'confirmationUrl' : confirmationUrl,
            'url' : url,
        }

        return render(
            request,
            'payments/checkout.html',
            ctx
        )

    @classmethod
    @method_decorator(csrf_exempt)
    def confirmation(self, request):
        if settings.DEBUG:
            apiKey     = '4Vj8eK4rloUd272L48hsrarnUA'
        else:
            apiKey     = 'IXltfYxCYPA2efIuyqj3L8k3uG'
        
        if request.method == "POST":
            print ("POST")
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
            signature = hashlib.md5(signature).hexdigest()

            user = reference_sale.split('_')

            if signature == sign:
                user = Staff.objects.filter(pk=user[1])
                invoice = Invoice.objects.filter(user=user, is_discharged=False).last()

                #Aprobada
                if state_pol == '4':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference_pol
                    invoice.payment_status = Invoice.APPROVED
                    invoice.is_discharged = True
                    invoice.save()
                    return HttpResponse(status=200)
                #Declinada
                elif state_pol == '6':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference_pol
                    invoice.payment_status = Invoice.REJECTED
                    invoice.is_discharged = False
                    invoice.save()
                    return HttpResponse(status=200)
                #Error
                elif state_pol == '104':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference_pol
                    invoice.payment_status = Invoice.CANCEL
                    invoice.is_discharged = False
                    invoice.save()
                    return HttpResponse(status=200)
                #Expirada
                elif state_pol == '5':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference_pol
                    invoice.payment_status = Invoice.CANCEL
                    invoice.is_discharged = False
                    invoice.save()
                    return HttpResponse(status=200)
                #Pendiente
                elif state_pol == '7':
                    invoice.payment_date = datetime.now()
                    invoice.payu_reference_code = reference_pol
                    invoice.payment_status = Invoice.PENDING
                    invoice.is_discharged = False
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
            signature = hashlib.md5(signature).hexdigest()

           
            if signature == signature_get:  

                return render(
                    request,
                    'payments/payment-resumen.html',
                    {
                        'merchand_id':merchand_id, 
                        'referenceCode':referenceCode,
                        'transactionState':transactionState,
                        'value':value,
                        'currency':currency,
                        'id_compra':referenceCode,
                        'reference_pol': reference_pol,
                        'polPaymentMethodType': polPaymentMethodType,
                    }
                    
                ) 
        else:
            return HttpResponseNotAllowed("Método no permitido")
