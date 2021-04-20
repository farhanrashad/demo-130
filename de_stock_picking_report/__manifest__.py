# -*- coding: utf-8 -*-
{
    'name': "Stock Picking",
    'summary': """Stock Picking Summary""",
	'description': """
    This Module Reflects Changes on Transfers on Quantity Calculation Field
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",

    'category': 'Warehouse',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'report/report_stockpicking_operations.xml',
        'views/stock_picking_views.xml',
        # 'security/ir.model.access.csv',
    ],

}
