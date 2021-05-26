# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions(<http://www.technaureus.com/>).

{
    'name': 'POS Order Notes ',
    'version': '13.0.1.9',
    'category': 'Point of Sale',
    'summary': 'Order and Line notes in POS Interface',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'description': """Notes on POS Orders and Order lines.
    Also print on receipt.
    """,
    'price': 15,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'depends': ['point_of_sale'],
    'data': [
        'views/import.xml',
        'views/pos_config.xml',
        'views/pos_order_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': ['static/src/xml/*.xml'],
    'images': ['images/main_screenshot.png'],
    'live_test_url': 'https://www.youtube.com/watch?v=UZ3ut4Dl0EY'
}
