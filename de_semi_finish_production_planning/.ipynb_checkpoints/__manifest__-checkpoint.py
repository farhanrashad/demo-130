# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Semi Finish Production Planning",
    "category": 'Education',
    "summary": 'Finish Production Summary',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.1',
    "depends": ['base','mrp','purchase'],
    "data": [
        # 'security/ir.model.access.csv',
        'views/finish_production_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}