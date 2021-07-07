# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    disc = fields.Float(string='Discount', store=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.depends('order_line.disc')
    def _discount_tot(self):
        for order in self:
            discs = 0.0
            for line in order.order_line:
                discs += line.disc
            order.update({
                'discount': round(discs,2),
            })
    
    
    
   

    discount = fields.Monetary(string='Disc.%', compute='_discount_tot', store=True)
    tot_after_discount = fields.Monetary(string='Total After Discount', compute='_amount_after_discount')
    total_disc = fields.Monetary(string='Total', compute='_disount_grand_tot')
    
    
    @api.depends('discount')
    def _amount_after_discount(self):
        test = self.amount_untaxed * (self.discount/100)
        self.tot_after_discount = self.amount_untaxed - test
       
    
    
    @api.depends('tot_after_discount')
    def _disount_grand_tot(self):
        for order in self:
            order.update({
                'total_disc': order.tot_after_discount + order.amount_tax
            })
   
    
    
    
    
    


