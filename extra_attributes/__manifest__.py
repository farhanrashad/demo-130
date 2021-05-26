# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Product Extra Attributes",
    
    "author": "Softhealer Technologies",
    
    "website": "https://www.softhealer.com",
        
    "support": "support@softhealer.com",

    "version":"13.0.9",
    
    "category": "Product",
    
    "summary": "",
        
    "description": """    
    """,
     
    "depends": ['base', 'product','sale','stock', 'account', 'point_of_sale', 'purchase'],
    
    "data": [
        'security/ir.model.access.csv',
        'views/fabric_view.xml',
        'views/product_quality_view.xml',
        'views/season_view.xml',
        'views/year_view.xml',
        'views/collection_view.xml',
        'views/fabric_consumption_view.xml',
        'views/fit_view.xml',
        'views/style_view.xml',
        'views/design_code_view.xml',
        'views/product_view.xml',
        'views/stock_quant_view.xml',
        'views/pos_order_view.xml',
        'views/purchase_view.xml',
        'reports/account_invoice_report_view.xml',
        'reports/sale_report_view.xml',
    ],
    
    "installable": True,
    "auto_install": False,
    "application": True,
}
