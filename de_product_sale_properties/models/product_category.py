# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class ProductCateogry(models.Model):
    _inherit='product.category'
    
    category_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('style', 'Style'),
        ], string='Category Type')
    
    property_factory_ref_no = fields.Char('Fact. Pattern Ref.')
