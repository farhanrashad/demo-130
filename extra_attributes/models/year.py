# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields, api, _


class Year(models.Model):
    _name = 'attribute.year'
    _description = "Year"
    _rec_name = 'name'
    name = fields.Char("Year", required=True)
    year_product_ids = fields.One2many(
        'product.template',
        'product_year_id',
        string='Year',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_compute_products_count',
    )
    
    @api.depends('year_product_ids')
    def _compute_products_count(self):
        for year in self:
            year.products_count = len(year.year_product_ids)
