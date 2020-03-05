from odoo import models, api, fields


class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.message.wizard.invoicing'

    user_id = fields.Many2one('res.partner', string="Recipient")
    mobile = fields.Char(related='user_id.mobile', required=True)
    message = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message and self.mobile:
            message_string = ''
            message = self.message.split(' ')
            for msg in message:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.user_id.mobile + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }


class Whatsappinventoryreciept(models.TransientModel):
    _name = 'whatsapp.message.wizard.stock'

    user_id_reciept = fields.Many2one('stock.picking', string="Recipient")
    mobile_reciept = fields.Char(related='user_id_reciept.mobile_reciept',required=True)  # related='user_id_reciept_s.mobile_reciept'
    origin_reciept = fields.Char(related='user_id_reciept.origin',required=True)  # related='user_id_reciept_s.mobile_reciept'
    message_reciept = fields.Text(string="message", required=True)

    def send_message(self):
        if self.message_reciept and self.mobile_reciept:
            message_string = ''
            message_reciept = self.message_reciept.split(' ')
            for msg in message_reciept:
                message_string = message_string + msg + '%20'
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.user_id_reciept.mobile_reciept + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }
