from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InternalTransferStock(models.Model):
    _inherit = 'stock.move'

    barcode = fields.Char(string='Barcode', related='product_id.barcode')


class InternalTransferPOS(models.Model):
    _inherit = 'pos.order'

    barcode = fields.Char(string='Barcode', related='product_id.barcode')
