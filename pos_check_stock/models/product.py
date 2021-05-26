# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_stock_data(self, config_id):
        pos_config = self.env['pos.config'].browse(config_id)
        location_ids = pos_config.location_ids
        stock_data = []
        qty = 0.0
        for location in location_ids:
            domain = [
                '|', ('location_id', 'in', [location.id]),
                ('location_id', 'child_of', location.id),
                ('product_id', '=', self.id)
            ]
            quants = self.env['stock.quant'].sudo().search(domain)
            qty = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
            stock_data.append({'location': location.complete_name, 'qty': qty})
        return stock_data
