# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.
{
    'name' : 'Ticket Excel Report',
    'version': '13.0',
    'author': 'Dynexel Pvt.Ltd.',
    'category': 'Helpdesk',
    'license': 'LGPL-3',
    'summary': 'Excel sheet for Ticket',
    'description': """ Ticket excel report""",
    'depends': [
        'de_helpdesk','base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
