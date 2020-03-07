# -*- coding: utf-8 -*-
{
    'name': "Employee Disciplinary Action",

    'summary': """
       Employee Disciplinary Action
       """,

    'description': """
           Employee Disciplinary Action
           1- Disciplinary Action
           2- Disciplinary Case
           this is version 0.2 to improve some feature
           like 
           1- Remove Extra Added Button
           2- Drop Down added for action type.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'reports/report.xml',
        'reports/disciplinary_case.xml',
        'data/sequence.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
