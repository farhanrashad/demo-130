# -*- coding: utf-8 -*-
{
    'name': "Account Workflow",

    'summary': """
    Accounting Workflow
    Payment
    Invoices
        """,

    'description': """
        Accounting workflow(Approvals) including invoices, payments
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_payment_views.xml',
        'views/payment_report_template.xml',
        'views/account_move_views.xml',
        'views/report_account_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
