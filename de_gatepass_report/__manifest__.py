# -*- coding: utf-8 -*-
{
    'name': "Gatepass & Delivery Report",
    'summary': """ Gatepass Report """,
    'description': """Gatepass Report for DUT""",
    "sequence": 5,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'inventorty gatepass report',
    # 'version': '14.0.0.0',
    'depends': ['base','stock'],
    
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/gatepass_report.xml',
        'views/gatepass_report_menu.xml',
        

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
