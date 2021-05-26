# -*- coding: utf-8 -*-
{
    'name': 'DXL Sale Discount Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop'],
    'data': [
        'views/sale_discount_report_xls.xml',
        'wizard/sale_discount_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}