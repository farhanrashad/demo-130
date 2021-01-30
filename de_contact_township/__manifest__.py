# -*- coding: utf-8 -*-
{
    'name': "Contact Townships",

    'summary': """
        Townships field on Contact Form
""",

    'description': """
         Townships field on Contact Form
         1- Township  menu in Purchase app
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Contact',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_township_views.xml',
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
