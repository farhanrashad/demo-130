# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Analytic Account",
    "summary": 'POS Analytic Account',
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '14.0.0.3',
    "depends": ['base','point_of_sale'],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_analytic_account_views_inherit.xml',
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
