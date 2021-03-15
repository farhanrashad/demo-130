# -*- coding: utf-8 -*-
{
    'name': "Inventory Gatepass",

    'summary': """
        Inventory Gatepass
        """,

    'description': """
        Inventory Gatepass 
    """,
    "sequence": 0,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Inventory',
    'version': '12.0.0.5',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'report/gatepass_template.xml',
        'report/gatepass_report.xml',
        'security/ir.model.access.csv',
        'data/gp_sequence.xml',
        'views/stock_move_line_views.xml',
        'views/gatepass_views.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
