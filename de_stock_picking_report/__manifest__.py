# -*- coding: utf-8 -*-
{
    'name': "Picking Report",
    
    'summary': """Picking Report""",
    
    'description': """Stock Picking Report""",
    
    'author': "Dynexcel",
    
    'website': "http://www.dynexcel.com",
    
    'category': 'Inventory',
    
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        
        'views/stock_picking_views.xml',
        'report/report_stockpicking_operations.xml',
    ],
   
}