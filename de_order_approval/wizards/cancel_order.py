# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'

    def action_cancel_order_wizard(self):
        order = self.env['sale.order'].browse(self.env.context.get('active_ids'))
        order.write({'cancel_reason': self.cancel_reason_id.id})
        return order.action_cancel_sale_order()

    cancel_reason_id = fields.Many2one('cancel.order.reason', string='Cancel Reason')
