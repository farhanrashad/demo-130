# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Modern POS Theme",
    "version": "13.0.1.7",
    "category": "Point Of Sale",
    "sequence": 1,
    "summary": "POS Theme, Make your pos screen beautiful with this theme.",
    "description": """POS Theme, Make your pos screen beautiful with this theme.
    """,
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com/",
    "depends" : ["point_of_sale"],
    "data" : [
            "views/assets.xml",
            "views/pos_config_view.xml",
            "views/res_config_settings_views.xml",
    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "price": 40,
    "currency": "EUR",
    "support": "support@softhealer.com",
    "live_test_url": "https://www.youtube.com/watch?v=ePkG_gQrS7A",
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
