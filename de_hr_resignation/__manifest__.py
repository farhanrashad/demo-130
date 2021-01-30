# -*- coding: utf-8 -*-
{
    'name': 'Open HRMS Resignation',
    'version': '13.0.2.0.0',
    'summary': 'Handle the resignation process of the employee',
    'author': 'Dynexcel',
    'company': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'depends': ['hr', 'de_hr_employee_updation', 'mail'],
    'category': 'Generic Modules/Human Resources',
    'maintainer': 'Dynexcel',
    'demo': ['data/demo_data.xml'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/resign_employee.xml',
        'views/hr_employee.xml',
        'views/resignation_view.xml',
        'views/approved_resignation.xml',
        'views/resignation_sequence.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
}

