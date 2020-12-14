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
    'name': "Age Verification",

    'summary': """
    Website
        """,

    'description': """
        Website age verification
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base','website'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  5,
    "currency"             :  "EUR",
    "license"              :  "Other proprietary",
    "live_test_url"        :  "https://youtu.be/oJ049abU_Kw",
    
    'demo': [
        'demo/demo.xml',
    ],
    
}
