# -*- coding: utf-8 -*-
{
    'name': "Stock Valuation Report",

    'summary': """
        Stock Valuation PDF & Excel Report.
        """,

    'description': """
        Features:
        1. Stock Valuation report on sales price
        2. This report only work with Fixed pricelist, Formula based pricelist is not compatible
        3. Support Community/Enterpris Edition
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'warehouse',
    'version': '13.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','report_xlsx'],

    # always loaded
    'data': [
        'wizard/product_stock_wizard_view.xml',
        'views/product_stock_report.xml',
        'views/product_stock_report_template.xml',
    ],

}