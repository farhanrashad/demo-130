# -*- coding: utf-8 -*-
{
    'name': 'DXL FBR Invoice Reports',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop', 'pos_promotion_niq'],
    'data': [
        'views/fbr_invoice_report_xls.xml',
        'wizard/fbr_invoice_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}