# -*- coding: utf-8 -*-
{
    'name': 'DXL Sale Summary Reports',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop', 'extra_attributes', 'pos_promotion_niq'],
    'data': [
        # 'security/stock_security.xml',
        'views/stock_report_xls.xml',
        'wizard/stock_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}