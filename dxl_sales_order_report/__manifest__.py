# -*- coding: utf-8 -*-
{
    'name': 'Ecommerce Order Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['sale', 'report_xlsx'],
    'data': [
    	'views/sale_report_xls.xml',
        'wizard/sale_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}