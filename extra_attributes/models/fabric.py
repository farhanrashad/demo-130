# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models, fields, api, _


class Fabric(models.Model):
    _name = 'attribute.fabric'
    _description = "Fabric"
    _rec_name = 'name'
    
    name = fields.Char("Fabric", required=True)
    fabric_product_ids = fields.One2many(
        'product.template',
        'product_fabric_id',
        string='Fabric',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_compute_products_count',
    )
    
    @api.depends('fabric_product_ids')
    def _compute_products_count(self):
        for fabric in self:
            fabric.products_count = len(fabric.fabric_product_ids)

    
class fabric_consumption(models.Model):
    _name = 'fabric.consumption'
    _description = 'Fabrci Composition'
    _rec_name = 'name'
    
    name = fields.Char("Fabric Composition")


class Fit(models.Model):
    _name = 'attribute.fit'
    _description = 'attribute fit'
    _rec_name = 'name'
    
    name = fields.Char("Fit")


class Collection(models.Model):
    _name = 'attribute.collection'
    _description = 'attribute collection'
    _rec_name = 'name'
    
    name = fields.Char("Collection")


class Style(models.Model):
    _name = 'attribute.style'
    _description = 'attributec style'
    _rec_name = 'name'
    
    name = fields.Char("Style")
    
