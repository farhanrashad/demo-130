# -*- coding: utf-8 -*-
{
    'name': "HR Training",

    'summary': """
                Hr Training Program
                """,

    'description': """
        Hr Training Program- This Module will provide all the information related to courses and session in the training program.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Training',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr', 'l10n_cn'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/training.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
