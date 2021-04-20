# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
#     sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=False)
    sum_qty_add = fields.Float(string='Total Quantity', compute='_quantity_add_all', store=False)

    
    @api.depends('move_ids_without_package.product_uom_qty')
    def _quantity_add_all(self):
        sum_qty = 0.0
        for mv in self:
            sum_qty = 0.0
            for line in mv.move_ids_without_package:
                sum_qty += line.product_uom_qty
            mv.sum_qty_add = sum_qty
            
#     @api.depends('move_line_ids.qty_done')
#     def _quantity_all(self):
#         """
#         Compute the total Quantity and Weight of the SO.
#         """
#         sum_qty = 0.0
#         for mv in self:
#             sum_qty = 0.0
#             for line in mv.move_line_ids:
#                 sum_qty += line.qty_done
#             mv.sum_qty = sum_qty





#     @api.constrains('move_line_ids.product_id','move_line_ids.product_uom_qty')
#     def _quantity_all(self):
#         """
#         Compute the total Quantity and Weight of the SO.
#         """
#         sum_qty = 0.0
#         for mv in self:
# #             sum_qty = 0.0
#             for line in mv.move_line_ids:
#                 sum_qty += line.product_uom_qty
#             mv.sum_qty = sum_qty

#     @api.onchange('move_line_ids.product_id','move_line_ids.product_uom_qty')
#     def _quantity_all(self):
#         total = 0
#         for rec in self:
#             for line in rec.move_line_ids:
#                 if rec.move_line_ids:
#                     total += line.product_uom_qty
#                 rec.sum_qty = total
                
                
                
                
#      def quantity_sum(self):
#         for record in self:
#           discount_total = 0.0
#             for line in record.order_line:  
#                 discount_total += line.x_price_discount_amount
#                 record['x_price_discount_amount_total'] = discount_total
            
