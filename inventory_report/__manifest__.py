# -*- coding: utf-8 -*-

{
    'name': 'Inventory Report',
    'version': '13.0',
    'category': 'stock',
    'description': """ Inventory Report """,
    'summary': 'Inventory Report',
    'depends': ['stock', 'resupply_stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/inventory_report_template.xml',
    ],
    'installable': True,
    'application': True,
}
