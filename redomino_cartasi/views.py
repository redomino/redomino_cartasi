# coding=utf-8
import logging

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from lfs.plugins import PAID
from lfs.order.models import Order
from lfs.order.settings import CANCELED
from lfs.order.settings import PAYMENT_FAILED
from lfs.caching.utils import lfs_get_object_or_404
from lfs.checkout.views import thank_you as _original_thank_you

from redomino_cartasi.utils import transaction2order_id
from redomino_cartasi.utils import log
from redomino_cartasi.utils import log_debug


def postform_cartasi(request, template='postform_cartasi.html'):
    """ Form with auto redirect to cartasi """
    return render(request, template, request.REQUEST)

@csrf_exempt
def error(request, template='error.html'):
    """ Error buying view """
    try:
        log_debug("ERROR during payment for %s" % str(request.POST))
        transaction_id = request.POST.get('TRANSACTION_ID')
        log_debug("transaction id %s should be cancelled (ERROR STATE)" % transaction_id)
        order_id = transaction2order_id(transaction_id)
        log("Order %s should be cancelled (ERROR STATE)" % order_id)
        order = lfs_get_object_or_404(Order, pk=order_id)
        order.state = PAYMENT_FAILED
        order.save()
        log("Order %s cancelled (ERROR)" % order_id)
    except Exception, e:
        log("An error has occurred cancelling order (PAYMENT ERROR) %s [%s]" % (str(request.POST), str(e)))
    return render(request, template, request.REQUEST)

@csrf_exempt
def annulment(request, template='annulment.html'):
    """ Annulment view """
    try:
        log_debug("Annullment requested for %s" % str(request.POST))
        transaction_id = request.POST.get('TRANSACTION_ID')
        log_debug("transaction id %s should be cancelled" % transaction_id)
        order_id = transaction2order_id(transaction_id)
        log("Order %s should be cancelled" % order_id)
        order = lfs_get_object_or_404(Order, pk=order_id)
        order.state = CANCELED
        order.save()
        log("Order %s cancelled" % order_id)
    except Exception, e:
        log("An error has occurred cancelling order %s [%s]" % (str(request.POST), str(e)))
    return render(request, template, request.REQUEST)

@csrf_exempt
def paid_cartasi(request):
    """
    Cartasi documentation (italian only).

    Formato VPOSNotification
    ========================
    
    Pag 49, messaggio http inviato con metodo POST, in modalità SSL.
    
    Rappresenta il messaggio inoltrato da X-PAY agli URL (NOTIFICATION_URL e RESULT_URL) 
    specificati dall’esercente nel messaggio di apertura dell’ordine (VPOSReqFull o nel 
    nostro caso VPOSReqLight), per potergli comunicare l’esito positivo della transazione. 
    La comunicazione verso il NOTIFICATION_URL avviene tramite una chiamata diretta server 
    to server, quella verso il RESULT_URL avviene tramite il browser dell’acquirente.
    
    Parametri:
    
        * TERMINAL_ID
    
        * TRANSACTION_ID
    
        * RESPONSE -> TRANSACTION_OK
    
        * AUTH_CODE -> alfanum max 10 char (codice auth ricevuto dall'emittente della carta di credito, anche con spazi)
    
        * TRANSACTION_DATE -> gg/mm/aaaa hh.mm.ss
    
        * CARD_TYPE -> tipo carta usata (es VISA)
    
        * AMOUNT
    
        * CURRENCY
    
        * TRANSACTION_TYPE, tipo transazione con livelli di sicurezza (vedi App A2)
    
        * MAC
    
        Es: TERMINAL_ID=0000000050242004&TRANSACTION_ID=T000000000000000001&RE
        SPONSE=TRANSACTION_OK&AUTH_CODE=901867&TRANSACTION_DATE=06/07/2005
        16.55.56&CARD_TYPE=VISA&AMOUNT=000123056&CURRENCY=978
        &TRANSACTION_TYPE=VBV_FULL&MAC=70C4F1F621A5DED95C7EE8C5507A9E1F297
        0BCFE&REGION=Europe&COUNTRY=Italy&PRODUCT_TYPE=Consumer&LIABILITY_
        SHIFT=N
    
    
        I parametri utilizzati per il calcolo
        questo tipo di messaggio sono i seguenti:
        o TERMINAL_ID
        o TRANSACTION_ID
        o RESPONSE
        o AMOUNT
        o CURRENCY
        o Chiave per MAC

        Al termine ritorna una VPOSNotificationRes

        Formato VPOSNotificationRes
        ===========================
        Pag 58.

        Messaggio http inviato con metodo POST, in modalità SSL

        RESPONSE -> 0 (operazione elaborata correttamente)
    """

    try:
        response = request.POST['RESPONSE']
        if response == 'TRANSACTION_OK':
            transaction_id = request.POST['TRANSACTION_ID']
            log("Received TRANSACTION OK for %s" % transaction_id)
            order_id = transaction2order_id(transaction_id)
            log_debug("internal order id: %s" % transaction_id)
            order = lfs_get_object_or_404(Order, pk=order_id)
            order.state = PAID
            order.save()
            log("TRANSACTION SAVED for %s" % transaction_id)
            return 'RESPONSE=0'
        else:
            log("WARNING, received a non TRANSACTION_OK for %s" % str(request.POST))
    except Exception, e:
        log("AN ERROR IS OCCURRED FOR request %s [%s]" % (str(request.POST), str(e)))

@csrf_exempt
def thank_you(request, template_name="lfs/checkout/thank_you_page.html"):
    """ We need to redefine the thank you view (cartasi sends a POST with a csrf failure)"""
    return _original_thank_you(request, template_name)

