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
    'summary': """Report for customer's outstanding invoice amount within the particular date period""",
    'website': 'http://www.dynexcel.com',
    'license': 'AGPL-3',
    'description': """
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
