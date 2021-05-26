# -*- coding: utf-8 -*-
{
    'name': 'Shop Wise Profit Report XLS',
    'version': '13.0',
    "category": "Project",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop'],
    'data': [
        # 'security/pos_security.xml',
        'security/ir.model.access.csv',
        'views/analytic_region_view.xml',
    	'views/pos_report_xls.xml',
        'wizard/shop_wise_profit_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}