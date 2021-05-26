# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields, api, _


class Season(models.Model):
    _name = 'attribute.season'
    _description = "Season"
    _rec_name = 'name'
    
    name = fields.Char("Season", required=True)
    season_product_ids = fields.One2many(
        'product.template',
        'product_season_id',
        string='Season',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_compute_products_count',
    )
    
    @api.depends('season_product_ids')
    def _compute_products_count(self):
        for season in self:
            season.products_count = len(season.season_product_ids)
