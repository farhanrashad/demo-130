# -*- coding: utf-8 -*-

{
    'name' : 'POS Invoice Integration',
    'version' : '1.0',
    'summary': 'POS Invoice Integration',
    'description': """POS Invoice Integration""",
    'depends' : ['point_of_sale', 'product_harmonized_system'],
    'data': [
        'views/assets.xml',
        'views/pos_config.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'application': False,
}   
