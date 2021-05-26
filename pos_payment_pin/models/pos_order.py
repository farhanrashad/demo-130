# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    cc_pin = fields.Char('Card Number')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['cc_pin'] = ui_order['cc_pin']
        return res

    def add_payment(self, data):
        pos_order_id = data.get('pos_order_id')
        pos_order = self.browse(pos_order_id)
        payment_method_id = data.get('payment_method_id')
        payment_method = self.env['pos.payment.method'].browse(payment_method_id)
        if (payment_method.is_credit_card and pos_order.cc_pin):
        	data['cc_pin'] = pos_order.cc_pin
        return super(PosOrder, self).add_payment(data)

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_credit_card = fields.Boolean('Is Credit Card ?')


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    cc_pin = fields.Char('Card Number')

