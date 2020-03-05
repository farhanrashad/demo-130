# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockReceipt(models.Model):
    _inherit = 'stock.picking'

    def send_msg(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.message.wizard.stock',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id_reciept': self.id},
                }


class StockField(models.Model):
    _inherit = 'stock.picking'

    mobile_reciept = fields.Char(string='Mobile', tracking=True,
                                 required=True)  # mobile = fields.Char(string='Mobile',  required=True)

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
