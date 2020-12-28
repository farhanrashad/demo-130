
{
    'name': '[10% OFF] WhatsApp Integration',
    'version': '13.0.0.1.0',
    'summary': 'Send Message/SaleOrders/Invoices/Employee Handling via just one click',
    'description': """Odoo is a fully integrated suite of business modules that encompass the traditional ERP functionality.
        Use Odoo Whatsapp Integration to send messages, SalesOrders, Quotations, Reminders, Invoices
        and Employee handling on just one click.""",
    'category': 'Contacts',
    'author': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'price': 99,
    'currency': 'EUR',
    'company': 'Dynexcel',
    'website': 'https://www.dynexcel.com',
    'depends': [
        'base', "sale_management", 'hr', 'contacts', 'purchase', 'stock'
        ],
    'data': [
        'wizard/whatsapp_message_wizard.xml',
        'wizard/whatsapp_message_payment.xml',
        'wizard/whatsapp_message_wizard_employee.xml',
        'wizard/whatsapp_message_wizard_stock.xml',
        'wizard/message_wizard.xml',
        'security/ir.model.access.csv',
        'data/ir_action_server.xml',
        'views/account_move_view.xml',
        'views/account_payment_view.xml',
        'views/detail_log_view.xml',
        'views/hr_employee_view.xml',
        'views/purchase_order_view.xml',
        'views/res_config_setting_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/whatsapp_message_view.xml',
        'views/whatsapp_setting_view.xml',
        'views/menu_item.xml',

    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': '',
}
