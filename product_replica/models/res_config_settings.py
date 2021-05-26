# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_replica = fields.Boolean(string='Product Replica', config_parameter='product_replica.is_replica')
    suffix = fields.Char(string="Suffix", config_parameter='product_replica.suffix')
    product_quality_id = fields.Many2one('product.quality', string="Product Quality", config_parameter='product_replica.product_quality_id')
