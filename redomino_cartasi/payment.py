import urllib

from django.conf import settings

from lfs.plugins import PaymentMethodProcessor
from lfs.plugins import PM_ORDER_IMMEDIATELY

from redomino_cartasi.conf import MAC_KEY
from redomino_cartasi.conf import TERMINAL_ID
from redomino_cartasi.conf import ACTION_CODE
from redomino_cartasi.conf import CURRENCY
from redomino_cartasi.conf import LANGUAGE
from redomino_cartasi.conf import NOTIFICATION_URL
from redomino_cartasi.conf import RESULT_URL
from redomino_cartasi.conf import ERROR_URL
from redomino_cartasi.conf import ANNULMENT_URL
from redomino_cartasi.conf import VERSION_CODE
from redomino_cartasi.conf import MESSAGE_TYPE
from redomino_cartasi.conf import CO_PLATFORM
from redomino_cartasi.conf import VPOS_ACTION

from redomino_cartasi.utils import get_mac
from redomino_cartasi.utils import log_debug
from redomino_cartasi.utils import log


class CartasiPaymentMethodProcessor(PaymentMethodProcessor):
    """
    Implements the Cartasi payment processor.
    """

    def process(self):
        return {
            "accepted": True,
            "next_url": self.get_pay_link(),
        }

    def get_create_order_time(self):
        return PM_ORDER_IMMEDIATELY

    def get_pay_link(self):
        total = self.order.price
        # cartasi requires a POST while LFS performs a GET
        # We redirect to a form that performs a POST to cartasi
        TRANSACTION_ID = "T%019d" % self.order.id
        AMOUNT = "%09d" % int(total*100)
        EMAIL = self.order.customer_email
        DESC_ORDER = '%s %s' % (self.order.customer_firstname, self.order.customer_lastname)
        code = ''.join([TERMINAL_ID,
                        TRANSACTION_ID,
                        AMOUNT,
                        CURRENCY,
                        VERSION_CODE,
                        CO_PLATFORM,
                        ACTION_CODE,
                        EMAIL,
                        MAC_KEY
                       ]
                      )
        log("CODE: %s" % code)

        MAC = get_mac(code)
        log_debug("MAC: %s" % MAC)

        data = {
                'TRANSACTION_ID': TRANSACTION_ID,
                'AMOUNT': AMOUNT,
                'TERMINAL_ID': TERMINAL_ID,
                'ACTION_CODE': ACTION_CODE,
                'CURRENCY': CURRENCY,
                'LANGUAGE': LANGUAGE,
                'NOTIFICATION_URL': NOTIFICATION_URL,
                'RESULT_URL': RESULT_URL,
                'ERROR_URL': ERROR_URL,
                'ANNULMENT_URL': ANNULMENT_URL,
                'VERSION_CODE': VERSION_CODE,
                'MESSAGE_TYPE': MESSAGE_TYPE,
                'CO_PLATFORM': CO_PLATFORM,
                'DESC_ORDER': DESC_ORDER,
                'MAC': MAC,
                'EMAIL': EMAIL,
                'ACTION': VPOS_ACTION,
               }

        
        url_string =  urllib.urlencode(data)
        log_debug("ok for MAC %s" % MAC)
        return "cartasi/postform_cartasi?%s" % url_string
