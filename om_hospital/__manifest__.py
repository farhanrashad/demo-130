# -*- coding: utf-8 -*-
{
    'name': 'Usama Shakeel',
    'version': '14.0.1.0.0',
    'summary': 'Odoo 14 Development ',
    'sequence': -100,
    'description': """Odoo 12 Development """,
    'category': 'Productivity',
    'author': 'Odoo Mates',
    'maintainer': 'Usama Shakeel',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'data/sequence.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}