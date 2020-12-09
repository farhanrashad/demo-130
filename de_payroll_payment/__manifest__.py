# -*- coding: utf-8 -*-
{
    'name': "Payroll Payment",

    'summary': """
       Payroll Payment""",

    'description': """
        Payroll Payment
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/payroll_payment_views.xml',
        'wizards/payroll_payment_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
