# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount = fields.Float(string='Disc.%', store=True)
    tot = fields.Char(string='Total After Discount', compute='_amount_after_discount', store=True)
    
    
    @api.depends('amount_untaxed', 'discount')
    def _amount_after_discount(self):
        test = self.amount_untaxed * (self.discount/100)
        self.tot = self.amount_untaxed - test
#             order.update({
#                 'amount_untaxed': amount_untaxed,
#                 'amount_tax': amount_tax,
#                 'amount_total': amount_untaxed + amount_tax,
#             })

    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
