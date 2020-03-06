# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderApproval(models.Model):
    _inherit = 'sale.order'

    def submit_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'

    def action_cancel_sale_order(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        self.message_post(body=_('Payment has approved and posted by %s,') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])
        res = super(SaleOrderApproval, self).action_confirm()
        return res

    cancel_reason = fields.Many2one('cancel.order.reason', string='Cancel Reason', index=True,
                                    track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('sale', 'Sale Order'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], readonly=True, string='Status')


class CancelReason(models.Model):
    _name = "cancel.order.reason"
    _description = 'Cancel sale order reason'

    name = fields.Char('Description', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
