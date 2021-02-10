# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Material Requirement Report",
    "category": 'Stock',
    "summary": 'Material Requirement Report By Dynexcel',
    "description": """
	 This module is generating the pdf reports of the material requirement.
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.0.0.0',
    "depends": ['base','stock'],
    "data": [
        'security/ir.model.access.csv',
        'reports/material_requirement_report.xml',
        'reports/material_requirement_template.xml',
        'views/material_requirement_view.xml',
        'views/view.xml',
        'wizard/material_requirement_wizard_view.xml',
    ],

    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}