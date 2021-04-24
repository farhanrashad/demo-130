# -*- coding: utf-8 -*-
{
    'name': "Purchase Requisition",
    'summary': """
    Purchase Requistion or Demand
        """,
    'description': """
        Purchase Requisition:-
        Create purchase requisitions for RFQs
        Print purchase requisition
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Purchase',
    'version': '14.0.0.2',
    'depends': ['base','purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/purchase_demand_type_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_demand_views.xml',
        'reports/purchase_requisition_report.xml',
        'reports/report_purchaserequisition.xml',
    ],
}
