# -*- coding: utf-8 -*-
{
    'name': "Order Approvals",
    'summary': """Purchase Order Approvals""",
    'description': """Purchase Order Approvals""",
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Human Resource',
    'version': '14.0.0.1',
    'depends': ['base', 'approvals', 'purchase'],
    'data': [
        'views/approval_request_views.xml',
    ],
}