# -*- coding: utf-8 -*-
{
    'name': "Warehouse Transfer",

    'summary': """
    Warehouse Stock Transfer
        """,

    'description': """
    Warehouse Stock Transfer
    1 - Transfer from Warehouse A to Warehouse B
    2 - Create Stock picking
        """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/sequence.xml',
        'security/security.xml',
        # 'wizards/picking.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
