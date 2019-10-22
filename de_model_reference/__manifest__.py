# -*- coding: utf-8 -*-
{
    'name': "Model Reference",

    'summary': """
    Self References
        """,

    'description': """
        Extra References
        1 - Self Reference Product Template 
        2 - Sale Order Reference in PO
        3- Sale Order Reference in Picking
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','purchase','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}