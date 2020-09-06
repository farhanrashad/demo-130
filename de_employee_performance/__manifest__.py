# -*- coding: utf-8 -*-
{
    'name': "Employee Performance",

    'summary': """
    KRA/KPI
        """,

    'description': """
        Employee key reasults areas and key performance indicators
    """,

    'author': "dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/kra_views.xml',
        'views/project_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
