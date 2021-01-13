# -*- coding: utf-8 -*-
{
    'name': "Project and Task Templates",

    'summary': """
        Creating Project and Task Templates""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/project_template_view.xml',

        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
}
