# -*- coding: utf-8 -*-
{
    'name': "Job Order",

    'summary': """
        Job Order Sheet""",

    'description': """
        Job Order Planning
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Job Order',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/job_order_sheet.xml',
        'data/sheet_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
