# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Hide Product Price",
    "author" : "Softhealer Technologies",
    "website": "http://www.softhealer.com",
    "support": "info@softhealer.com",    
    "category": "Sales",
    "description": """This module useful to hide product price from other users""",    
    "version":"13.0",
    "depends" : ["product", "stock"],
    "application" : True,
    "data": [
        "security/hide_price_security.xml",            
        "views/hide_price_view.xml",            
    ],            
    "images": ["static/description/background.png",],              
    "auto_install":False,
    "installable" : True,
    "price": 8,
    "currency": "EUR"      
}
