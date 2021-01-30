# -*- coding: utf-8 -*-
{
    'name': "PriceList Modifications",

    'summary': """
        Extend functionality of Price Lists.""",

    'description': """
        Extend functionality of Price Lists.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'PriceList',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/product_pricelist_ext.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
