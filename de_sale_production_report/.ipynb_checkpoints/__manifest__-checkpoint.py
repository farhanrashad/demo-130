# -*- coding: utf-8 -*-
{
    'name': "Sale Manufacturing Order Report",

    'summary': """
                 Print Manufacturing order which contain Sale Reference 
                """,

    'description': """
                 Print Manufacturing order which contain Sale Reference 
                 1- MO number
                 2- product 
                 3- quantity
                 4- shade
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sale_production_report.xml',
        'report/sale_production_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
