# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    reference_product_tmpl_id = fields.Many2one('product.template', 'Reference Product', ondelete='cascade', required=False)

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100