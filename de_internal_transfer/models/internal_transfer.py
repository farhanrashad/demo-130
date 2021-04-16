from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InternalTransfer(models.Model):

    _inherit = 'stock.move'


    barcode = fields.Char(string='Barcode', related='product_id.barcode')