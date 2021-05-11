# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
    
class product_properties(models.Model):
    _name='product.properties'
    _description='Product Properties'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
 
    name=fields.Char('Name')
    product_property_order_line=fields.One2many('product.properties.line','product_property',string="Product Properties")
    is_short = fields.Boolean(string="Is Short") 
    is_long = fields.Boolean(string="Is Long")
    categ_id = fields.Many2many('product.category', string="Category")
    long_sequence = fields.Integer(string='Long Sequence', required=True, default=10)
    short_sequence = fields.Integer(string='Short Sequence', required=True, default=10)

class product_property_line(models.Model):
    _name='product.properties.line'
    
    product_property=fields.Many2one("product.properties",string="Product Property Order") 
    name = fields.Char(string="Short Value",required=True)
    description = fields.Char(string="Long Value",required=False)
    property_factory_ref_no = fields.Char('Fact. Pattern Ref.')
