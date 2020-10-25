# -*- coding: utf-8 -*-
{
    'name': "Task Sub Task Checklist",

    'summary': """
        Task Sub Task Checklist
        """,

    'description': """
        With the help of this module you can divide task or sub task into list of activities,
         so task and subtask progress will easily control in Odoo project management
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/task_checklist.xml',
        'views/checklist_activity_stages.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
