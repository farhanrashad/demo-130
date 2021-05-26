# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    visible_in_reporting = fields.Boolean(string="Visible in Custom Reporting")
