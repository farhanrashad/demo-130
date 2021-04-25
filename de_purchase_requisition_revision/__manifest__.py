# -*- encoding: utf-8 -*-
{
    "name": "Purchase Requisition Revision",
    "version": "14.0.0.0",
    "author": "Dynexcel",
    "website": "http://www.dynexcel.com",
    "sequence": 1,
    "depends": ["purchase", "de_purchase_requisition"],
    "category": "Purchase",
    "description": """Purchase revision history""",
    "data": [
        'views/purchase_req_revision_views.xml',
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
