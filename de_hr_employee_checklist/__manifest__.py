# -*- coding: utf-8 -*-
{
    'name': "HR Employee Checklist",

    'summary': """
        HR Employee Entry and Exit Checklist""",

    'description': """
        Normally when we hire any employee we need to collect some documents from employee and need to provide 
        some document to them from our end but because of some workload if we miss something we can not track it.
        Using this application we can maintain full checklist for entry and exit process which can be configured
         based on requirement.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/hr_employee_checklist.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
