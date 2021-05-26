# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Import Sale Order Lines from CSV/Excel file",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "summary": "This module useful to import sale order lines from csv/excel.",
    "description": """
    
 This module useful to import sale order lines from csv/excel. 
 

                    """,
    "version":"13.0.1",
    "depends" : ["base", "sh_message", "sale_management", "sale"],
    "application" : True,
    "data" : ['security/import_sol_security.xml',
            'wizard/import_sol_wizard.xml',
            'views/sale_view.xml',
            ],
    'external_dependencies' : {
        'python' : ['xlrd'],
    },
    "images": ["static/description/background.png", ],
    "auto_install":False,
    "installable" : True,
    "price": 15,
    "currency": "EUR"   
}
