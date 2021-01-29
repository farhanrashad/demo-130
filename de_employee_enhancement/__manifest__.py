# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Employee Enhancement",
    "category": 'Education',
    "summary": 'Employee Form and Contract Enhancement',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['sale'],
    "data": [
#         'security/ir.model.access.csv',
#         'security/security.xml',
        'views/hr_employee_view.xml',
    ],
    
    "price": 100,
    "currency": 'PKR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
