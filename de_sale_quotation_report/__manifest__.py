# -*- coding: utf-8 -*-

{
    "name": "Purchase Order Quotation Report",
    'version': '14.0.0.0',
    "category": 'Purchase Order Quotation Report',
    "summary": ' Purchase Order Quotation Report',
    'sequence': -7,
    "description": """"  """,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    'license': 'LGPL-3',
    'depends': ['base','purchase','sale'],
    'data': [


        'report/purchase_quotation_report.xml',
        'views/purchase_order_quotation_report.xml',

    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}

