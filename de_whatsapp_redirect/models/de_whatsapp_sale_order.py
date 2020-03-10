# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def send_message(self):
        if  self.mobile_sale:
            message_string = "Hello, \n your order {name} amount is $ {amount_total}  has been confirmed. \n".format(
                name=str(self.name),amount_total=self.amount_total)
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.mobile_sale + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }


    # def send_msg(self):
    #     return {'type': 'ir.actions.act_window',
    #             'name': _('Whatsapp Message'),
    #             'res_model': 'whatsapp.message.wizard.sale',
    #             'target': 'new',
    #             'view_mode': 'form',
    #             'view_type': 'form',
    #             'context': {'default_sale_order_id': self.id},
    #             }

class StockField(models.Model):
    _inherit = 'sale.order'

    mobile_sale = fields.Char(string='Mobile', tracking=True, required=True)
    message_sale = fields.Char(string='Message', tracking=True)
