# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class IrActionsServer(models.Model):

    _inherit = 'ir.actions.server'

    state = fields.Selection(selection_add=[
        ('tel_sms', 'Telenor Send SMS'),
    ])

    telenor_sms_template_id = fields.Many2one('send_sms',string="SMS Template", ondelete='set null', domain="[('model_id', '=', model_id)]",)

    @api.model
    def run_action_tel_sms(self, action, eval_context=None):
        if not action.sms_template_id or not self._context.get('active_id'):
            return False

        template = action.sms_template_id
        active_model = self._context.get('active_model')
        sms_body = template._render_template(template.body, template.model, self.env.context.get('active_id') or 0)
        record_id = self.env[active_model].browse(self.env.context.get('active_id'))
        if not record_id and not record.partner_id and not record.partner_id.mobile:
            return False 
        data = {
            'res_model': active_model,
            'res_id': record_id.id,
            'partner_id': record_id.partner_id.id,
            'mobile': record_id.partner_id.mobile,
            'message': sms_body,
        }
        self.env['telenor.sms'].send(data)
        return True
