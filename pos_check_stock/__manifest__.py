# -*- coding: utf-8 -*-
{
    "name" : "POS Check Inventory",
    "version" : "13.0.1.1",
    "category" : "Point of Sale",
    'summary': 'POS Check Inventory',
    "author": "Preciseways",
    "depends" : ['stock', 'point_of_sale'],
    "data": [
        'views/pos_assets.xml',
        'views/pos_config.xml',
    ],
    'qweb': [
        'static/src/xml/pos_stock.xml',
    ],
    "auto_install": False,
    "installable": True,
}
