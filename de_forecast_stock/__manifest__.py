# -*- coding: utf-8 -*-
{
    'name': "Forecast Stock",
    'version': '14.0.0.1',
    'summary': """Purchase order based on sale order
    """,
    'sequence': '1',
    'description': """
    """,
    'category': 'productivity',
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    'version': '0.1',
    'depends': [ 'sale'],
    'data': [
        'views/pending_bill_notify.xml',
    ],

    'demo': [
    ],
    'installable': 'True',
    'application': 'True',
    'auto-install': False,
}
