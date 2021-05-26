# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields, api, _


class ProductQuality(models.Model):
    _name = 'product.quality'
    _description = "Product Quality"
    _rec_name = 'name'
    
    name = fields.Char("Product Quality", required=True)
    quality_product_ids = fields.One2many(
        'product.template',
        'product_quality_id',
        string='Product Quality',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_compute_products_count',
    )
    
    @api.depends('quality_product_ids')
    def _compute_products_count(self):
        for quality in self:
            quality.products_count = len(quality.quality_product_ids)
