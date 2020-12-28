from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
import datetime
import base64
import re
from datetime import datetime


class ResHRModel(models.Model):
    _inherit = 'hr.employee'

    message_counter_employee = fields.Integer('Message Counter')
    message_highliter = fields.Char('Message Highlight')
    history_count = fields.Integer('History Counter', compute='history_counter')
    counter_wizard = fields.Char('Counter')

    def send_msg(self):
        # print('xyz')
        cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
        credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard.employee',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_contacts_to': [[6, 0, [self.id]]],
                            'default_whatsapp_account': credetionals.id,
                            'default_record_id': self.id,
                            'default_model_name': str(self._inherit)
                            },
                }

    def wa_history(self):
        return {
            'name': (_('WhatsApp History')),
            'domain': [('from_model', '=', 'Employee'), ('employee_name', '=', self.id)],
            'view_type': 'form',
            'res_model': 'detail.logs',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def history_counter(self):
        self.history_count = len(self.env['detail.logs'].search([('from_model', '=', 'Employee'), ('employee_name', '=', self.id)]))

    def multi_send_msg(self):
        # print("xyz")

        cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
        credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard.employee',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                # 'res_id': new_id.id,
                'context': {
                    'default_contacts_to': [[6, 0, self.ids]],
                            'default_whatsapp_account': credetionals.id,
                            # 'default_record_id': self.id,
                            'default_model_name': str(self._inherit),
                    'default_selection_check': 0,
                    'default_invisible_check': 1,
                },
                }
