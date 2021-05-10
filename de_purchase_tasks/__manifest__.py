# -*- coding: utf-8 -*-
{
    'name': "Purchase Order to Project",

    'summary': """
            """,

    'description': """
        
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'purchase'],
    # always loaded
    'data': [
        'views/project_task_view.xml',
        'views/project_view.xml',
        'views/purchase_order_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
