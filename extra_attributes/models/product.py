# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    product_fabric_id = fields.Many2one('attribute.fabric', string="Fabric", store=True)
    product_quality_id = fields.Many2one('product.quality', string="Product Quality", store=True)
    product_season_id = fields.Many2one('attribute.season', string="Season", store=True)
    product_year_id = fields.Many2one('attribute.year', string="Year", store=True)
    launch_date = fields.Date(string="Launch Date", store=True)
    product_fit_id = fields.Many2one('attribute.fit', string="Fit", store=True)
    fabric_consumption_id = fields.Many2one('fabric.consumption', string="Fabric Composition", store=True)
    collection_id = fields.Many2one('attribute.collection', string="Collection", store=True)
    style_id = fields.Many2one('attribute.style', string="Style", store=True)        
    sku = fields.Char(string="SKU")
    design_code_id = fields.Many2one('design.code','Design Code')
    product_id = fields.Char("Product ID",compute='get_id')
    
    def get_id(self):
        str_id=''
        if self:
            for rec in self:
                str_id+= str(rec.id)
                rec.product_id = str_id
                
class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    product_fabric_id = fields.Many2one('attribute.fabric', string="Fabric", related="product_tmpl_id.product_fabric_id", store=True)
    product_quality_id = fields.Many2one('product.quality', string="Product Quality", related="product_tmpl_id.product_quality_id", store=True)
    product_season_id = fields.Many2one('attribute.season', string="Season", related="product_tmpl_id.product_season_id", store=True)
    product_year_id = fields.Many2one('attribute.year', string="Year", related="product_tmpl_id.product_year_id", store=True)
    launch_date = fields.Date(string="Launch Date", related="product_tmpl_id.launch_date", store=True)
    product_fit_id = fields.Many2one('attribute.fit', string="Fit", related="product_tmpl_id.product_fit_id", store=True)
    fabric_consumption_id = fields.Many2one('fabric.consumption', string="Fabric Composition", related="product_tmpl_id.fabric_consumption_id", store=True)
    collection_id = fields.Many2one('attribute.collection', string="Collection", related="product_tmpl_id.collection_id", store=True)
    style_id = fields.Many2one('attribute.style', string="Style", related="product_tmpl_id.style_id", store=True) 
    sku = fields.Char(string="SKU", related="product_tmpl_id.sku", store=True)
    design_code_id = fields.Many2one('design.code','Design Code')
    product_id = fields.Char("Product ID",compute='get_id')
    
    def get_id(self):
        str_id=''
        if self:
            for rec in self:
                str_id+= str(rec.id)
                rec.product_id = str_id
