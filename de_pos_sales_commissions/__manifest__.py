{

    'name': 'Pos sales Commissions',
    'summary': 'Sales Commissions in Point of Sales',
    'author': 'Dynexcel',
    'depends':
        [
            'base','sale','sales_team','hr_payroll','hr','point_of_sale','account',
        ],
    'data':
        [
            'security/ir.model.access.csv',
            'security/security.xml',
            'reports/report_commission.xml',
            'views/commission_rule_view.xml',
            'views/commission_summary_view.xml',
            'views/commission_view.xml',
            'views/commission_payment_view.xml',
            'views/pos_sales_views_inherit.xml',
        ],
    'installable': True,

}