# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    sum_qty = fields.Float(string='Total ',  store=False, readonly=True , compute='_quantity_all')



    @api.depends('move_ids_without_package')
    def _quantity_all(self):
        
        for rec in self:
            total = 0
            for line in rec.move_ids_without_package:
                total =  total + line.product_uom_qty
            rec.sum_qty = total