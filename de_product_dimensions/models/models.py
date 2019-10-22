# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Product(models.Model):
    _inherit = 'product.template'

    length = fields.Char(string='Length',)
    width = fields.Char(string='Width',)
    height = fields.Char(string='Height',)
    
    secondary_unit_qty = fields.Float(string='Unit Quantity',default=1.0,required=True)

    #secondary_uom_id = fields.Many2one( 'uom.uom', string='Secondary (UOM)', stored=True, help="Default Unit of Measure used for dimension.")
    secondary_uom_id = fields.Many2one('uom.uom', 'Secondary UOM', required=True, Help="Alternative or secondary Unit of measurement")
    secondary_qty_available = fields.Float(string="Secondary Unit of Measure", compute='get_secondary_qty_available')
    
    @api.depends('secondary_uom_id')
    def get_secondary_qty_available(self):
        for record in self:
            record.secondary_qty_available = record.qty_available
            if record.secondary_uom_id:
                record.secondary_qty_available = record.qty_available * record.secondary_unit_qty
    