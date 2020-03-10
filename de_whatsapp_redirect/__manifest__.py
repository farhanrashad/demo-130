# -*- coding: utf-8 -*-
{
    'name': "Send Whatsapp Message",

    'summary': """
            Send Whatsapp Message        
               """,

    'description': """
           Send Whatsapp Message
           1- Send Messaage From Invoicing
           2- Send Message From Sale Order, Purchase Order, Inventory receipt and Delivery Order
           3- when click on button the same window will appear but message will auto generate for all 
              details and line items like sale order print or purchase order print...
               """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/de_whatsapp_sale_order.xml',
        'views/de_whatsapp_purchase_order.xml',
        'views/de_whatsapp_invoicing_customer.xml',
        'views/de_whatsapp_inventory_stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
