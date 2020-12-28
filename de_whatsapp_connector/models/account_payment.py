from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import requests
import json
import datetime
import base64
import re
from datetime import datetime



class ResPayments(models.Model):
    _inherit = 'account.payment'

    msg_count_pay = fields.Integer('Message Counter')
    msg_highlite = fields.Char('Message Highlight')
    message_sales = fields.Char('Message Payment')
    history_count = fields.Integer('History Counter', compute='history_counter')

    def send_msg(self):
        # print('xyz')

        report_id = self.env.ref('account.action_report_payment_receipt')
        if report_id:
            pdf, data = report_id.sudo()._render(self.id)
            pdf64 = base64.b64encode(pdf)
            attachment_invoice = self.env['ir.attachment'].create(
                {
                    # "name": f"{self.type_name} - {self.name}",
                    "name": self.display_name,
                    'type': 'binary',
                    "datas": pdf64
                }
            )

        cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
        credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

        payment_check = self.env['ir.config_parameter'].sudo().get_param(
            'de_whatsapp_connector.payment')

        if payment_check:
            self.message_sales = f"""Hello {self.partner_id.name},\nPlease Acknowledge Attached {self.state} Report.\n
The {self.state} "{self.name}" Contain Following Information\n"""
            self.message_sales += f"""----------------------------\nAmount: {self.amount}\nJournal: {self.journal_id.name}\nDate: {self.date}\n----------------------------"""

        else:
            self.message_sales = ''

        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard.payments',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_contacts_to': [[6, 0, self.partner_id.ids]],
                            'default_whatsapp_account': credetionals.id,
                            'default_attatchments_whatsap': [[6, 0, [attachment_invoice.id]]],
                            'default_record_id': self.id,
                            'default_message': self.message_sales,
                            'default_model_name': str(self._inherit),
                            # 'default_contacts_to': 1,
                            },
                }

    def whatsapp_payments(self):
        try:
            cre_id = self.env['ir.config_parameter'].sudo().get_param('de_whatsapp_connector.select_account_whatsapp')
            credetionals = self.env['whatsapp.settings'].search([('id', '=', cre_id)])

            if not credetionals:
                raise UserError('You Have Not Selected Whatsapp Account or Forget to Save Creditionals!')
            # else:
            #     self.name = credetionals.id

            if not self:
                raise UserError('You Have Not Selected Any Payments!')

            instance = credetionals.whatsapp_instance_id
            token = credetionals.whatsapp_token

            header = {
                'Content-type': 'application/json',
            }

            for order in self:

                contact = order.partner_id
                if not contact.country_id.phone_code:
                    raise UserError(f'"{contact.name}" Recipient does not contain Country. Select Country First!')

                signature_check = self.env['ir.config_parameter'].sudo().get_param(
                    'de_whatsapp_connector.whatsapp_signature')

                payment_check = self.env['ir.config_parameter'].sudo().get_param(
                    'de_whatsapp_connector.payment')

                if payment_check:
                    order.message_sales = f"""Hello {order.partner_id.name},\nPlease Acknowledge Attached {order.state} Report.\n
The {order.state} "{order.name}" Contain Following Information\n"""
                    order.message_sales += f"""----------------------------\nAmount: {order.amount}\nJournal: {order.journal_id.name}\nDate: {order.date}\n----------------------------"""

                else:
                    order.message_sales = f'Hello {contact.name},\nPlease Acknowledge Attached {order.display_name} Report. \n'

                if signature_check:
                    signature_str = ''
                    signature_list = re.findall("\>(.*?)\<", self.env.user.signature)
                    for signature in signature_list:
                        if signature:
                            signature_str += signature

                    order.message_sales += '\n \n--' + signature_str + '--'

                phone = str(contact.country_id.phone_code) + contact.mobile[-10:]

                if len(phone) < 11 or len(phone) > 13:
                    raise UserError(f'"{contact}" Might Have Wrong Phone Number!')

                url = f"https://eu38.chat-api.com/instance{instance}/sendMessage?token={token}"

                responce_status_code = 0
                data = json.dumps({"phone": phone, "body": order.message_sales})
                responce = requests.post(url, data, headers=header)
                responce_status_code = responce.status_code

                report = self.env.ref('account.action_report_payment_receipt').report_action(order)
                report_id = self.env.ref('account.action_report_payment_receipt')
                pdf, data = report_id.sudo()._render(order.id)
                pdf64 = base64.b64encode(pdf)
                attachment_id = self.env['ir.attachment'].create(
                    {
                        "name": f"{order.state}",
                        "datas": pdf64
                    }
                )

                url_files = f"https://eu38.chat-api.com/instance{instance}/sendFile?token={token}"
                json_response_file = 0

                decode_data = attachment_id.datas.decode('utf-8')
                docode_file = f"data:{attachment_id.mimetype};base64," + decode_data
                data_file = {
                    "phone": phone,
                    'filename': attachment_id.name,
                    "body": docode_file
                }
                response_file = requests.request("POST", url_files, json=data_file, headers={})
                json_response_file = response_file.status_code
                # print('Ending')

                if responce_status_code == 200 or json_response_file == 200:
                    # self.message_sent_id = json_responce['id']

                    order.write({
                        'msg_count_pay': order.msg_count_pay + 1,
                    })
                    p = self.env['res.partner'].search([('id', '=', contact.id)])
                    x = p.message_counter + 1
                    p.write({
                        'message_counter': x,
                        'message_highliter': f'Whatsapp Messages:{x}'
                    })

                    message = self.env['mail.message'].create({
                        'subject': 'Whatsapp Message',
                        'body': 'Whatsapp Message:\n' + order.message_sales,
                        'attachment_ids': [[6, 0, [attachment_id.id]]],
                        'model': 'account.payment',
                        'res_id': order.id,
                        'no_auto_thread': True,
                        'add_sign': True,
                    })

                    channel_search = self.env['mail.channel'].search([('channel_partner_ids', '=', contact.id)])
                    if not channel_search:
                        self.env['mail.channel'].create({
                            # 'sl_slack_channel_id': channel_search.id,
                            'name': contact.name,
                            'alias_user_id': self.env.user.id,
                            'is_subscribed': True,
                            'is_member': True,
                            'channel_partner_ids': [[6, 0, [contact.id]]],
                            'channel_message_ids': [[4, message.id]],
                            # 'channel_message_ids': [[6, 0, [message.id]]]
                        })
                    else:
                        channel_search.write({
                            # 'sl_slack_channel_id': channel_search.id,
                            'name': contact.name,
                            'alias_user_id': self.env.user.id,
                            'is_subscribed': True,
                            'is_member': True,
                            'channel_partner_ids': [[6, 0, [contact.id]]],
                            'channel_message_ids': [[4, message.id]]
                            # 'channel_message_ids': [[6, 0, [message.id]]]
                        })
                    self.env.cr.commit()

                    logs = {
                        # 'sync_list_id': self.id,
                        'sync_date': datetime.now(),
                        'contact_name': contact.id,
                        'account_used': credetionals.id,
                        'message_sucess': 'Sucessful',
                        'files_attachted': [[6, 0, [attachment_id.id]]],
                        'signature_att': 'Yes' if signature_check else 'No',
                        'from_model': 'Account Payments'
                    }
                    self.env['detail.logs'].create(logs)
                    self.env.cr.commit()
                    continue
                else:
                    logs = {
                        # 'sync_list_id': self.id,
                        'sync_date': datetime.now(),
                        'contact_name': contact.id,
                        'account_used': credetionals.id,
                        'message_sucess': 'Error',
                        'files_attachted': [[6, 0, [attachment_id.id]]],
                        'signature_att': 'Yes' if signature_check else 'No',
                        'from_model': 'Account Payments'
                    }
                    self.env['detail.logs'].create(logs)
                self.env.cr.commit()
            else:
                context = dict(self._context)
                context['message'] = 'Sucessful!'
                return self.message_wizard(context)

        except Exception as e:
            logs = {
                # 'sync_list_id': self.id,
                'sync_date': datetime.now(),
                'contact_name': contact.id,
                'account_used': credetionals.id,
                'message_sucess': 'Error',
                'files_attachted': [[6, 0, [attachment_id.id]]],
                'signature_att': 'Yes' if signature_check else 'No',
                'from_model': 'Account Payments'
            }
            self.env['detail.logs'].create(logs)
            self.env.cr.commit()

            raise ValidationError(e)

    def wa_history(self):
        return {
            'name': (_('WhatsApp History')),
            'domain': [('from_model', '=', 'Account Payments'), ('contact_name', '=', self.partner_id.id)],
            'view_type': 'form',
            'res_model': 'detail.logs',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def history_counter(self):
        self.history_count = len(self.env['detail.logs'].search([('from_model', '=', 'Account Payments'), ('contact_name', '=', self.partner_id.id)]))

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












