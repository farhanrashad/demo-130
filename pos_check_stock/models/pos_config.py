# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning

class PosConfig(models.Model):
    _inherit = 'pos.config'

    check_stock = fields.Boolean(string='Allow Check Inventory')
    location_ids = fields.Many2many('stock.location')
