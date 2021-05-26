# -*- coding: utf-8 -*-
{
    'name': 'DXL Credit Card Summary Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop'],
    'data': [
        'views/card_summary_report_xls.xml',
        'wizard/card_summary_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}