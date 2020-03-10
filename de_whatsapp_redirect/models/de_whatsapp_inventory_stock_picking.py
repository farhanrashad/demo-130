# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockReceipt(models.Model):
    _inherit = 'stock.picking'

    def send_message(self):
        if self.mobile_reciept:
            message_string = "Hello, \n your order {name} Recieve By {partner_id}  has been confirmed. \n".format(
                name=str(self.name), partner_id=str(self.partner_id))
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.mobile_reciept + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }


class StockField(models.Model):
    _inherit = 'stock.picking'

    mobile_reciept = fields.Char(string='Mobile', tracking=True, required=True)

    # def send_message(self):
    #     # if self.message and self.mobile:
    #     #     message_string = ''
    #     #     message = self.message.split(' ')
    #     #     for msg in message:
    #     #         message_string = message_string + msg + '%20'
    #     #     message_string = message_string[:(len(message_string) - 3)]
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': "https://api.whatsapp.com/send?phone= " + self.mobile_reciept,  # + "&text=" + message_string,
    #         'target': 'self',
    #         'res_id': self.id,
    #     }

      # mobile = fields.Char(string='Mobile',  required=True)

    # def Action_whatsapp(self):
    #     template_id = self.env.ref('de_whatsapp_redirect.send_whatsapp_invoices')
    #     template_id.send_message(self)
    #     # template = self.env['mail.template'].browse(template_id)
        # template.send_mail(self, force_send=True)

# from odoo import models, fields, api


# class de_whatsapp_redirect(models.Model):
#     _name = 'de_whatsapp_redirect.de_whatsapp_redirect'
#     _description = 'de_whatsapp_redirect.de_whatsapp_redirect'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
