# -*- coding: utf-8 -*-
{
    'name': "Manufacturing Bom in Sale Order",

    'summary': """
        Bill of Material Selection on Sale Order Line""",

    'description': """
        This module provides functionality for sales users select bill of material of selected product in sale order line.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Manufacturing',
    'version': '0.1',

    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_ext.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
