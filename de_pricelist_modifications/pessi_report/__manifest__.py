# -*- coding: utf-8 -*-
{
    'name': "Pessi Report",

    'summary': """
        This module is for pesssi xlsx Report""",

    'description': """
        Long description of module's purpose
    """,

    'author': "qwexer",
    'website': "http://www.qwexer.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'HR',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx','hr_payroll','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}