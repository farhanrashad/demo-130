# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS Manager Validation in Odoo",
    "version" : "13.0.0.1",
    "category" : "",
    'summary': 'This module for pos manager validation.',
    "description": """This app is useful for validate and authenticate pos manager for add/remove quantity, change price, apply discount, remove order line, remove order, payment and close pos screen, also manager authenticate one time password for pos order.

Manager override on POS features
pos Manager override on POS
Manager permission in POS
pos manager Authorize
manager Authorize in pos 
pos manager authorization
pos manager privileges
manager privileges in pos 
pos Manager permission
POS double approval
pos manager approval
pos manager double approval
pos Manager Approve
Manager Approve
pos manager validate
pos manager double validate
pos manager allow
custom manager approvals
  manager Validation  
Validate POS Closing
Validate Order Deletion
Validate Order Line Deletion
Validate Order Payment
Validate Discount Application
Validate Price Change
Validate Decreasing Quantity
point of sale manager Validation in odoo

point of sale manager approval in odoo


Validate POS Closing
Validate pos Order Deletion
Validate pos Order Line Deletion
Validate pos Order Payment
Validate pos Discount Application
Validate pos Price Change
Validate pos Decreasing Quantity

    """,
    "author": "BrowseInfo",
    "website" : "www.browseinfo.in",
    "price": 29,
    "currency": 'EUR',
    "depends" : ['base','point_of_sale'],
    "data": [
        'views/pos_config.xml'
    ],
    'qweb': [
    'static/src/xml/pos.xml'
    ],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/f7Sp2FFwxjc',
    "images":["static/description/Banner.png"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
