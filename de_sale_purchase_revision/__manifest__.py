# -*- coding: utf-8 -*-
{
    'name': "Sale Purchase Revision",

    'summary': """
        Sale Purchase Revision By Dynexcel""",

    'description': """
        This Module works in sale and purchase to create revisions
    """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
    'category': 'Purchase Sale',
    'version': '14.0.0.0',

    'depends': ['base', 'purchase', 'sale'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_purchase_revision_view.xml',
    ],
}
