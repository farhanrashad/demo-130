# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>
#

#################################################################################

{
    'name': "Invoice Register",
    'author': 'Dynexcel',
    'category': 'account',
    'summary': """ Update Account Register
                   1- Sale Register
                   2- Purchase Register
    """,
    'website': 'http://www.dynexcel.com',
    'license': 'AGPL-3',
    'description': """
                Update Account Register for GMSA to print report
                1-Invoices which product_id true.
                2-multiple tax on single invoice product.
""",
    'version': '1.0',
    'depends': ['base','account'],
    'data': [
             'wizard/de_sale_register.xml',
             'wizard/de_purchase_register.xml',
             'views/de_invoice_register.xml',
             'report/de_sale_register_template.xml',
             'report/de_purchase_register_template.xml',
             'report/sale_register_report.xml',
             'report/purchase_register_report.xml',
             ],
    # 'installable': True,
    # 'images': ['static/description/banner.png'],
    # 'application': True,
    # 'auto_install': False,
}
