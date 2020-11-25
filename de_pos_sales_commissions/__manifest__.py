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
            'views/pos_sales.xml',
            'wizards/report_wizard.xml',
        ],
    'installable': True,

}