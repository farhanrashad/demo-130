# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, modules,fields, _

class ProjectTaskExt(models.Model):
    _inherit = 'product.template'

    style_code = fields.Char(string="Style Code")


