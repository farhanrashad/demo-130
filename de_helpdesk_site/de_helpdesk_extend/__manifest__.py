# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Repair View",

    'summary': """
        Custom Views for Reporting
        """,

    'description': """
        Custom Views for Reporting
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Helpdesk',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_helpdesk_site','de_helpdesk'],

    # always loaded
    'data': [
        'views/helpdesk_ext_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
