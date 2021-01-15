# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Leave Portal',
    'version': '12.0.0.0',
    'category': 'Time off',
    'sequence': 10,
    'summary': 'website time off ',
    'depends': [
        'hr_holidays',
        'portal',
        'rating',
        'resource',
        'web',
        'web_tour',
        'digest',
        'base',
    ],
    'description': "",
    'data': [
        'security/security.xml',
        'views/time_off_template.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

