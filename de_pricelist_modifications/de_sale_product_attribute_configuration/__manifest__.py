{

    'name': 'sale product attribute configuration',
    'description': 'For daily needs data',
    'author': 'Usman',
    'depends':
        [
            'base',
            'sale', 
            'product', 
            'sale_product_configurator' ,
        ],
    'data':
        [    
           
            'views/custom_sp.xml',
            'security/ir.model.access.csv'
        ],
    'installable': True,

}