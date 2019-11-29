# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<https://dynexcel.com/>)
# Copyright(c): 2015-Present dynexcel.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
{
    'name': "Website Hide Price",

    'summary': """
        Show/Hide Product Price at website""",

    'description': """
        Show/Hide product prices at website
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base','website_sale','auth_signup'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/website_hide_price.xml',
    ],
    "images"               :  ['static/description/banner.jpg'],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  5,
    "currency"             :  "EUR",
    "license"              :  "Other proprietary",
    "live_test_url"        :  "https://youtu.be/uCBdNkRjWh4",

    'demo': [
        'demo/demo.xml',
    ],
}