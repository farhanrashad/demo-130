from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
import datetime
import base64
import re
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    message_counter = fields.Integer('Message Counter')
    message_highliter = fields.Char('Message Highlight')
    history_count = fields.Integer('History Counter', compute='history_counter')
    last_msg_sent = fields.Char('Last Message Number')
    counter_wizard = fields.Char('Counter')
    # dicuss_history = fields.Char('Fetch History', compute='discuss_call')

    def send_msg(self):
        # print('xyz')

        cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
        credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

        # self.discuss_call()

        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_contacts_to': [[6, 0, [self.id]]],
                            'default_whatsapp_account': credetionals.id,
                            'default_record_id': self.id,
                            'default_model_name': str(self._inherit)},
                }

    def multi_send_msg(self):
        # print("xyz")

        cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
        credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

        # self.discuss_call()

        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard',
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

    def wa_history(self):
        return {
            'name': (_('WhatsApp History')),
            'domain': [('from_model', '=', 'Contacts'), ('contact_name', '=', self.id)],
            'view_type': 'form',
            'res_model': 'detail.logs',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def history_counter(self):
        self.history_count = len(self.env['detail.logs'].search([('from_model', '=', 'Contacts'), ('contact_name', '=', self.id)]))

    def discuss_call(self):
        try:
            # self.last_msg_sent = 0
            cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
            credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

            instance = credetionals.whatsapp_instance_id
            token = credetionals.whatsapp_token

            url = f"https://eu38.chat-api.com/instance{instance}/messages?token={token}&last={20}&chatId={str(self.country_id.phone_code) + self.mobile[-10:]}@c.us&limit={20}"

            header = {
                'Content-type': 'application/json',
            }

            responce = requests.get(url, headers=header)
            responce_status_code = responce.status_code
            responce_json = responce.json()['messages']

            msg_ids = []
            for msg in responce_json:
                message = None
                if msg['fromMe'] == False and msg['messageNumber'] > int(self.last_msg_sent) and msg['type'] == 'chat':
                # if msg['fromMe'] == False and msg['type'] == 'chat':
                    message = self.env['mail.message'].create({
                        'subject': 'Whatsapp Message',
                        'body': f'From {self.name}: ' + msg['body'],
                        # 'attachment_ids': [[6, 0, self.attatchments_whatsap.ids]],
                        # 'model': self.model_name,
                        # 'res_id': contact.id,
                        'no_auto_thread': True,
                        'add_sign': True,
                    })
                    self.last_msg_sent = str(msg['messageNumber'])
                    # msg_ids.append(message.id)

                    channel_search = self.env['mail.channel'].search([('channel_partner_ids','=', self.id)])
                    if not channel_search and message:
                        self.env['mail.channel'].create({
                            # 'sl_slack_channel_id': channel_search.id,
                            'name': self.name,
                            'alias_user_id': self.env.user.id,
                            'is_subscribed': True,
                            'is_member': True,
                            'channel_partner_ids': [[6, 0, self.ids]],
                            'channel_message_ids': [[4, message.id]],
                        })
                    else:
                        if message:
                            channel_search.write({
                                # 'sl_slack_channel_id': channel_search.id,
                                'name': self.name,
                                'alias_user_id': self.env.user.id,
                                'is_subscribed': True,
                                'is_member': True,
                                'channel_partner_ids': [[6, 0, [self.id]]],
                                'channel_message_ids': [[4, message.id]],
                            })
            self.env.cr.commit()

        except Exception as e:
            pass

    def wa_discuss(self):
        # self.discuss_call()

        channel = self.env['mail.channel'].search([('name', '=', self.name)])
        if not channel.is_member and not channel.is_subscribed:
            channel.write({
                'is_member': True,
                'is_subscribed': True,
            })

        self.ensure_one()
        channel_partner = channel.mapped('channel_last_seen_partner_ids').filtered(
            lambda cp: cp.partner_id == self.env.user.partner_id)
        # if not channel_partner:
        #     return channel.write({'channel_last_seen_partner_ids': [(0, 0, {'partner_id': self.env.user.partner_id.id})]})

        return {'type': 'ir.actions.client',
                'res_model': 'mail.channel',
                'tag': 'mail.widgets.discuss',
                'context': {'active_id': f'mail.channel_{channel.id}'}
                # 'context': {'active_id': channel.id}
                }



















