# -*- coding: utf-8 -*-
{
    'name': "Minutes of Meeting",

    'summary': """
       Minutes of meetings and task can be added
       """,

    'description': """
        Using this application, You can add your Minutes Of meeting , You can take a PDF copy and can also send it
         through mail. It has a provision to allocate tasks for a respective project to multiple users.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'calendar',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'calendar', 'pad_project', 'project', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/send_email.xml',
        'data/email_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'reports/mom_pdf.xml',
        'reports/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
