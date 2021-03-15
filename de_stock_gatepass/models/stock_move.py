# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    gatepass_id = fields.Many2one('stock.gatepass', string='Gatepass')
    gatepass_qty = fields.Float(string='Gatepass Quantity')