# -*- coding: utf-8 -*-

{
    "name": "Product Replica",
    "version": "13.0.0.2",
    "category": "Product",
    "depends": ['stock'],
    "description": """This module is use for duplicate product.""",
    "data": [
        "security/stock_security.xml",
        "views/res_config_settings_view.xml",
        "views/product_view.xml",
    ],
    "installable": True,
    "application": True,
}
