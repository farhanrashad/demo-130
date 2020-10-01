# -*- coding: utf-8 -*-
{

    'name': "Pos sales Commissions",
    'summary': "This module allows to give commission to Sales Person.",
    'description': "This module is tested and working in Odoo community edition but not tested in Enterprise version. "
                   "And we are supporting Ubuntu OS and not Windows OS.",
    'author': 'dynexcel',
    'category': 'Point Of Sale',
    'depends':
        [
            'base', 'sale', 'sales_team', 'om_hr_payroll', 'hr', 'point_of_sale', 'account',],
    'data':
        [
            'views/pos_sales.xml',
            'views/report_wizard.xml',
            'security/ir.model.access.csv',
        ],
    'installable': True,

}