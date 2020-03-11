# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class Picking(models.Model):
    _inherit = 'stock.picking'

    warehouse_trasnfer_id = fields.Many2one("stock.warehouse.transfer", string="Warehouse Transfer", required=False)
