# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "PO Custom PDF",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",
        
    "support": "support@softhealer.com",

    "version":"13.0.1",
    
    "category": "Purchase",
    
    "summary": "",
        
    "description": """    
    """,
     
    "depends": ['base', 'web','purchase','stock','account',"product_matrix"],
    
    "data": [
        'views/po_custom_pdf_template_view.xml',
    ],
    
    "installable": True,
    "auto_install": False,
    "application": True,
}
