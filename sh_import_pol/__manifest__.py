# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Import Purchase Order Lines from CSV/Excel file",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Purchases",
    "summary": "This module useful to import purchase order lines from csv/excel.",
    "description": """
    
 This module useful to import purchase order lines from csv/excel. 
  

                    """,
    "version":"13.0.1",
    "depends" : ["base", "sh_message", "purchase"],
    "application" : True,
    "data" : ['security/import_pol_security.xml',
            'wizard/import_pol_wizard.xml',
            'views/purchase_view.xml',
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
