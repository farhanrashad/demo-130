# -*- coding: utf-8 -*-
{
    'name': 'DXL Mobile Data Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop'],
    'data': [
    	'views/pos_report_xls.xml',
        'wizard/pos_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}