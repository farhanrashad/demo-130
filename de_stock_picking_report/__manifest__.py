# -*- coding: utf-8 -*-
{
    'name': "Picking Report",
    'summary': ""Picking Report""",
    'description': """Stock Picking Report""",
	'sequence':'-100',
    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
         'report/report_stockpicking_operations.xml',
        'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
