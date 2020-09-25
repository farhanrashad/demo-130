{

    'name': 'Pos sales Commissions',
    'description': 'For daily needs data',
    'author': 'dynexcel',
    'depends':
        [
            'base',
            'sale',
            'sales_team',
            'hr_payroll',
            'hr',
            'point_of_sale',
            'account',
            
            
        ],
    'data':
        [    
           
            'views/pos_sales.xml',
            'views/report_wizard.xml',
            'security/ir.model.access.csv',
        ],
    'installable': True,

}