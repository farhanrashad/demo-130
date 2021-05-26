# -*- coding: utf-8 -*-
{
    'name': 'DXL Product Life Cycle Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'pos_promotion_niq'],
    'data': [
    	'views/product_life_cycle_report_xls.xml',
        'wizard/product_life_cycle_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}