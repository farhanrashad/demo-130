# -*- coding: utf-8 -*-

{
    "name": "Telenor SMS",
    "version": "13.0.5",
    "summary": "Send SMS to customer from Odoo using Telenor SMS Gateway",
    "category": "Extra Tools",
    "depends": [
        'base',
        'mail',
        'sms',
        'sales_team',
        'purchase',
        'base_automation',
        'phone_validation',
        'point_of_sale',
        'bi_pos_multi_shop',
        'pos_promotion_niq',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/sms_data.xml',
        'security/sms_security.xml',
        'views/res_company_view.xml',
        'views/sms_view.xml',
        'views/res_partner_view.xml',
        'views/daily_sms_view.xml',
        'wizard/sms_send_wizard.xml',
    ],
    "installable": True,
    "application": False,
}
