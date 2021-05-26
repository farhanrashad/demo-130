# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_open_sms_wizard(self):
        view_id = self.env.ref('telenor_sms.sms_send_wizard_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Send SMS'),
            'res_model': 'sms.send.wizard',
            'target': 'new',
            'context': {'send_sms': 'single'},
            'view_mode': 'form',
            'views': [[view_id, 'form']],
        }
