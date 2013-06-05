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
#        # cartasi requires a POST while LFS performs a GET
#        # We redirect to a form that performs a POST to cartasi

        data = {
                'ORDER_ID': self.order.id,
               }

        url_string =  urllib.urlencode(data)
        return "cartasi/postform_cartasi?%s" % url_string
