# -*- coding: utf-8 -*-
{
    'name': "Sale Analysis Report",

    'summary': """Sale Analysis Report""",
    'description': """Sale Analysis Report""",
    'author': "Dynexcel",
    'sequence':1,
    'website': "https://www.dynexcel.com",
    'category': 'Point Of Sale',
    'version': '14.0.0.1',
    'depends': ['base','point_of_sale','de_product_sale_properties'],
    'data': [
        'views/view_sales_analysis.xml',
        'reports/sales_analysis_report.xml',
    ],
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
