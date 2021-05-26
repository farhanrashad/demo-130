# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_name = fields.Char(compute="compute_variant_name")

    def compute_variant_name(self):
        for product in self:
            product_combination = product.product_template_attribute_value_ids.mapped('name')
            variant_name = product.name
            if product_combination:
                variant_name =  variant_name + '('+', '.join(product_combination)+')'
            if product.default_code:
                variant_name = product.default_code + '-' + variant_name
            product.variant_name = variant_name

class ResCompany(models.Model):
    _inherit = 'res.company'

    pos_logo = fields.Binary(string="PoS Logo", readonly=False)
