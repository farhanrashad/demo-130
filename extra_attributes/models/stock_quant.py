# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_fabric_id = fields.Many2one('attribute.fabric', related="product_id.product_fabric_id", store=True)
    product_quality_id = fields.Many2one('product.quality', string="Product Quality", related="product_id.product_quality_id", store=True)
    product_season_id = fields.Many2one('attribute.season', string="Season", related="product_id.product_season_id", store=True)
    product_year_id = fields.Many2one('attribute.year', string="Year", related="product_id.product_year_id", store=True)
    launch_date = fields.Date(string="Launch Date", related="product_id.launch_date", store=True)
    product_fit_id = fields.Many2one('attribute.fit', string="Fit", related="product_id.product_fit_id", store=True)
    fabric_consumption_id = fields.Many2one('fabric.consumption', string="Fabric Composition", related="product_id.fabric_consumption_id", store=True)
    collection_id = fields.Many2one('attribute.collection', string="Collection", related="product_id.collection_id", store=True)
    style_id = fields.Many2one('attribute.style', string="Style", related="product_id.style_id", store=True)
