# -*- coding: utf-8 -*-
{
    'name': 'POS Summary Report XLS',
    'version': '13.0',
    "category": "Project",
    'depends': ['point_of_sale', 'report_xlsx', 'pos_cash_in_out_odoo', 'bi_pos_multi_shop'],
    'data': [
        'security/pos_security.xml',
    	'views/pos_report_xls.xml',
        'wizard/pos_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}