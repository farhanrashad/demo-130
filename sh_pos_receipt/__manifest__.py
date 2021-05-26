# -*- coding: utf-8 -*-
{
    "name": "SH POS Receipt",
    "version": "13.0.3.0",
    "category": "Point Of Sale",
    "sequence": 2,
    "summary": "Make pos receipt beautiful with this module.",
    "depends" : ["point_of_sale", 'tis_pos_order_notes'],
    "data" : [
        "views/assets.xml",
        "views/product_view.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
