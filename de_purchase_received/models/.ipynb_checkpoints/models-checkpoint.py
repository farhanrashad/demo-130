# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('quantity')
    def product_quantity(self):
        for line in self:
            sum_bill_qty = 0.0
            purchase_order = self.env['purchase.order'].search([('name','=',line.move_id.invoice_origin)])
            for purchase_line in purchase_order.order_line: 
                if line.product_id.id == purchase_line.product_id.id:
                    sum_bill_qty = sum_bill_qty + line.quantity + purchase_line.qty_invoiced
                    if  sum_bill_qty > purchase_line.qty_received:
                        raise UserError(_('You can only bill quantity' + ' ' + str(purchase_line.qty_received) +  'for product' + str(line.product_id.name)))    
                          
                        
            
            
        