# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def send_message(self):
        if self.mobile:
            message_string = "Hello, \n Your Customer Name is {name} and his permanent address is {contact_address}  has been confirmed. \n".format(
                name=str(self.name), contact_address=self.contact_address)
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.mobile + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }




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
