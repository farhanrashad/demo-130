# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Stock(models.Model):
    _inherit = 'stock.warehouse'

    code = fields.Char('Short Name', required=True, size=25, help="Short name used to identify your warehouse")
