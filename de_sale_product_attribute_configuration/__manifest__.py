{

    'name': 'sale product attribute configuration',
    'description': 'For daily needs data',
    'author': 'Usman',
    'depends':
        [
            'base',
            'sale', 
            'product',  
        ],
    'data':
        [    
           
            'views/custom_sp.xml',
            'security/ir.model.access.csv'
        ],
    'installable': True,

}