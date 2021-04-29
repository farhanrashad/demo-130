# -*- coding: utf-8 -*-

{
    "name": "Come Tax Report",
    'version': '14.0.0.0',
    "category": 'Come Tax Report',
    "summary": ' Come Tax Report',
    'sequence': 3,
    "description": """"  """,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    'license': 'LGPL-3',
    'depends': ['base','contacts','account_accountant'],
    'data': [


        'report/sales_tax_or_commercel_invoice.xml',
        'views/sales_commercel_invoice.xml',

    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}

