# -*- coding: utf-8 -*-
{
    'name': "Gatepass Report",
    'summary': """ Gatepass Report """,
    'description': """Gatepass Report for DUT""",
    "sequence": 1,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
    'category': 'inventorty gatepass report',
    'version': '13.0.0.0',
    'depends': ['base','stock'],
    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/gatepass_report.xml',
        'views/gatepass_report_menu.xml',   
    ],
   
}
