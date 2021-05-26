{
    'name': 'Stock Re-Supply',
    'author': ' usman',
    'version': '13.0.6.0',
    'company': 'Dymaxel',
    'depends': [
                'base',
                'purchase',
                'product',
                'sale',
                'account',
                'stock',
                'location_customize',
                'warehouse_stock_restrictions',
                ],
     'images':[
        'resupply_stock/static/description/carpet.png'],           
                
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/carpet_process.xml',
        'data/carpet_seq.xml',
           
            ],
     'application': True,       
    'installable': True,
}
