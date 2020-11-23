# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Analytic Account",
    "category": 'Point of Sales',
    "summary": 'POS Analytic Account',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.1',
    "depends": ['base','point_of_sale'],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_analytic_account_view.xml',
        'views/pos_analytic_account_views_inherit.xml',
    ],

    "price": 0,
    "currency": 'EUR',
    "installable": True,
    "application": False,
    "auto_install": False,
}
