# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('quantity')
    def _product_quantity(self):
        for line in self:
            purchase_order = self.env['purchase.order'].search([('name','=',line.move_id.invoice_origin)])
            for purchase_line in purchase_order.order_line: 
                if line.product_id.id == purchase_line.product_id.id:
                    if  line.quantity > (purchase_line.qty_received - purchase_line.qty_invoiced):
                        raise UserError(_('You can only bill quantity' + ' ' + str(purchase_line.qty_received - purchase_line.qty_invoiced) + ' ' + 'for product'+ ' ' + str(line.product_id.name)))    
                          
                        
            
            
        