redomino_cartasi
================

Cartasi (www.cartasi.it, also known as "XPay CARTASI") payment method processor (light version) for Django LFS ecommerce (http://getlfs.com).

Put into you settings.py module the right configuration, for example::

    # CARTASI settings
    MAC_KEY_CARTASI = 'your key'
    TERMINAL_ID_CARTASI = 'your terminal id'
    ACTION_CODE_CARTASI = 'AUT-CONT'
    CURRENCY_CARTASI = '978'
    LANGUAGE_CARTASI = 'ITA'
    NOTIFICATION_URL_CARTASI = 'cartasi/paid_cartasi'
    RESULT_URL_CARTASI = 'thank-you'
    ERROR_URL_CARTASI = 'cartasi/error'
    ANNULMENT_URL_CARTASI = 'cartasi/annulment'
    VERSION_CODE_CARTASI = '01.00'
    MESSAGE_TYPE_CARTASI = 'C00'
    CO_PLATFORM_CARTASI = 'L'
    VPOS_ACTION_CARTASI = 'https://your-vpos-action'


Repository:

    https://github.com/redomino/redomino_cartasi


Tests:

    $ ./bin/django test redomino_cartasi 


Authors
-------

* [@davidemoro] davide.moro@redomino.com - http://redomino.com
