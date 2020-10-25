# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Retail Price Tax Calculation",
    "author" : "Dynexcel",
    "website": "https://www.dynexcel.com",
    "support": "support@dynexcel.com",
    "category": "Account",
    "summary": " Retail Price Total in account move",
    "description": """
                 Retail Price Total
                 1-calculated from Retail Price invoice line column
                    """,
    "version":"13.0.2",
    "depends" : ["base","sale_management","account"],
    "application" : True,
    "data" : [
            'views/sh_product_view.xml',
            'views/de_account_move_view.xml',
            ],
    "images": ["static/description/background.png", ],
    "auto_install":False,
    "installable" : True,
}
