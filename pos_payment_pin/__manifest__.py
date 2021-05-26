# -*- coding: utf-8 -*-
{
    "name": "POS Payment PIN",
    "version": "13.0.2",
    "category": "Point Of Sale",
    "sequence": 2,
    "summary": "",
    "depends" : ["point_of_sale"],
    "data" : [
        "views/assets.xml",
        "views/pos_order.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
