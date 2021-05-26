# -*- coding: utf-8 -*-
{
    'name': 'DXL Internal Transfer Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'report_xlsx', 'bi_pos_multi_shop', 'resupply_stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_data.xml',
        'views/stock_report_xls.xml',
        'wizard/stock_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}