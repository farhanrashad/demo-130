from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
import datetime
import base64
import re
from datetime import datetime



class BoxSettings(models.Model):
    _name = 'whatsapp.settings'

    name = fields.Char(string='Instance Name', required=True)
    whatsapp_instance_id = fields.Char(string='WhatsApp ID', required=True)
    whatsapp_token = fields.Char(string='WhatsApp Token', required=True)
    image = fields.Binary()
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('close', 'Close')],
        readonly=True, string='State', default='draft')

    def get_qr_code(self):
        # print('df')
        header = {
            'Content-type': 'application/json',
        }

        if not self.whatsapp_token and not self.name and not self.whatsapp_instance_id:
            raise UserError('Please Enter Creditionals First!')

        url = f"https://eu38.chat-api.com/instance{self.whatsapp_instance_id}/qr_code?token={self.whatsapp_token}"

        response = (requests.request("GET", url, headers=header))

        self.image = base64.b64encode(response.content)
        self.env.cr.commit()

    def test_connection(self):
        try:
            header = {
                'Content-type': 'application/json',
            }
            url = f"https://eu38.chat-api.com/instance{self.whatsapp_instance_id}/status?token={self.whatsapp_token}"
            response = (requests.request("GET", url, headers=header)).json()
            if response['accountStatus'] == 'authenticated':
                context = dict(self._context)
                context['message'] = 'Connection Successful!'
                self.update({
                    'state': 'active'
                })
                return self.message_wizard(context)

            elif response['accountStatus'] == 'got qr code':
                self.get_qr_code()
                context = dict(self._context)
                context['message'] = 'Connection Successful!'
                self.update({
                    'state': 'active'
                })
                return self.message_wizard(context)

        except:
            raise UserError('Check Whatsapp Crediontionals')



    def get_logout(self):
        header = {
            'Content-type': 'application/json',
        }
        url = f"https://eu38.chat-api.com/instance{self.whatsapp_instance_id}/logout?token={self.whatsapp_token}"

        responce = requests.post(url, headers=header)
        json_responce = responce.json()
        if responce.status_code == 200 and json_responce['result'] == 'Logout request sent to WhatsApp':
            context = dict(self._context)
            context['message'] = 'Logout request sent to WhatsApp!'
            self.update({
                'state': 'close'
            })
            return self.message_wizard(context)



    def message_wizard(self, context):
        return {
            'name': ('Success'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context
        }
