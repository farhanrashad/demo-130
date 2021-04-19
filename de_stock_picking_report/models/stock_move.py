# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    sum_qty = fields.Float(string='Total Quantity', compute='_quantity_all', store=False, readonly=True)

    @api.depends('move_line_ids.qty_done')
    def _quantity_all(self):
        """
        Compute the total Quantity and Weight of the SO.
        """
        sum_qty = 0.0
        for mv in self:
            sum_qty = 0.0
            for line in mv.move_line_ids:
                sum_qty += line.qty_done
            mv.sum_qty = sum_qty
