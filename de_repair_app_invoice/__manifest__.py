# -*- coding: utf-8 -*-
{
    'name': "Repair App Invoice Modification",

    'summary': """
          Repair App Invoice Modification to create multiple invoices
       """,

    'description': """
          Repair App Invoice Modification to create multiple invoices
          1- Hide Create Invoice Button in header
          2- Add Create Part Invoice and Create Operation Invoice Button in header.
          3- Multiple Invoices Created In Which Part Page Data and Operation Page Data Show Separately 
          in draft invoices.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','repair'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/repair_invoice_multiple.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
