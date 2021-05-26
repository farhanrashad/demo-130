# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    sequence_ref = fields.Char(string='Sequence Ref', copy=False, readonly=True)

    def generate_seq(self):
        self.sequence_ref = self.env['ir.sequence'].next_by_code('stock.inventory')

    def _action_done(self):
        res = super(StockInventory, self)._action_done()
        self.generate_seq()
        return res