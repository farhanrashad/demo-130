# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SmsSendWizard(models.TransientModel):
    _name = "sms.send.wizard"

    partner_id = fields.Many2one('res.partner', string='Partner')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    mobile = fields.Char(related='partner_id.mobile')
    message = fields.Text()
    is_bulk = fields.Boolean()

    @api.model
    def default_get(self, fields):
        rec = super(SmsSendWizard, self).default_get(fields)
        if self.env.context.get('send_sms') and self.env.context.get('send_sms') == 'single':
            active_id = self._context.get('active_id')
            rec.update({
                'partner_id': active_id,
                'is_bulk': False,
            })
        else:
            active_ids = self._context.get('active_ids')
            rec.update({
                'is_bulk': True,
                'partner_ids': [(6, 0, active_ids)],
            })
        return rec

    def action_send_sms(self):
        mobile = ''
        if not self.is_bulk and self.partner_id and self.partner_id.mobile:
            self.env['telenor.sms'].send({'partner_id': self.partner_id.id, 'mobile': self.partner_id.mobile, 'message': self.message})
        if self.is_bulk and self.partner_ids and len(self.partner_ids.mapped('mobile')):
            for partner in self.partner_ids.filtered(lambda x: x.mobile):
                self.env['telenor.sms'].send({'partner_id': partner.id, 'mobile': partner.mobile, 'message': self.message})
