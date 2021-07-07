{

    'name': 'Helpdesk SLA Modification',
    'description': 'For daily needs data',
    'author': 'Usman',
    'depends':
        [
            'de_helpdesk',
            'mail',
            
            
        ],
    'data':
        [    
           
            'views/sla_modification.xml',
            'security/ir.model.access.csv'
            
        ],
    'installable': True,

}