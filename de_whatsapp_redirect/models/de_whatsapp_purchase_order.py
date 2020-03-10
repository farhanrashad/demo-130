# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrderbutton(models.Model):
    _inherit = 'purchase.order'

    def send_message(self):
        if  self.mobile_purchase:
            message_string = "Hello, \n your Purchase Order {name} at date and time {date_order}  has been confirmed.".format(
                name=str(self.name),date_order=self.date_order)
            message_string = message_string[:(len(message_string) - 3)]
            return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone= " + self.mobile_purchase + "&text=" + message_string,
                'target': 'self',
                'res_id': self.id,
            }



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    mobile_purchase = fields.Char(string='Mobile', tracking=True, required=True)
