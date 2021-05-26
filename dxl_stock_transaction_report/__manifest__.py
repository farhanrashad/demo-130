# -*- coding: utf-8 -*-
{
    'name': 'DXL Stock Transaction Report',
    'version': '13.0',
    "category": "Stock",
    'depends': ['point_of_sale', 'stock', 'report_xlsx', 'bi_pos_multi_shop'],
    'data': [
        'views/product_category_view.xml',
        'views/stock_transaction_report_xls.xml',
        'wizard/stock_transaction_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
