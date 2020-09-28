# -*- coding: utf-8 -*-
{
    'name': "Account Assets Number",

    'summary': """
           Account Assets Number in asset model.
           """,

    'description': """
           Account Assets Number
           1-
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_asset','hr'],

    # always loaded
    'data': [
        'data/sequence.xml',
        # 'security/ir.model.access.csv',
        'security/asset_groups.xml',
        'views/res_config_settings.xml',
        'views/account_asset_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
