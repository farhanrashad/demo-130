# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplateRef(models.Model):
    _inherit = 'product.template'
    
    ref_product_tmpl_id = fields.Many2one('product.template', 'Product Reference', stored=True, required=False)

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class ProductProductRef(models.Model):
    _inherit = 'product.product'
    
    ref_product_id = fields.Many2one('product.product', 'Variant Reference', stored=True, required=False)