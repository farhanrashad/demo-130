# -*- coding: utf-8 -*-
{
    'name': "Partner Modification",

    'summary': """
            Vendor Only active when its Qualify
            """,

    'description': """
        Their are some Qualification Stages for vendor
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Partner',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account','stock','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
