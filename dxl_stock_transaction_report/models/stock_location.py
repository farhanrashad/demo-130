# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    wh_id = fields.Many2one('stock.warehouse', string='Warehouse', compute='_compute_wh_id', store=True)

    @api.depends('parent_path')
    def _compute_wh_id(self):
        for loc in self:
            loc.wh_id = loc.get_warehouse().id or False
