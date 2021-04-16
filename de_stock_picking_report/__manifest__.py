# -*- coding: utf-8 -*-
{
    'name': "Stock Picking Report",

    'summary': """
        Stock Picking Summary
    """,

    'description': """
    this module reflects changes on transfers on quantity calculation field
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",

    'category': 'Warehouse',
    'version': '13.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'report/report_stockpicking_operations.xml',
        'views/stock_picking_views.xml',
    ],

}
