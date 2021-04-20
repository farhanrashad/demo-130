from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseOrderEnhancement(models.Model):
    _inherit = 'purchase.order'

    subject = fields.Char(string="Subject")


class PurchaseOrderEnhancementLine(models.Model):
    _inherit = 'purchase.order.line'

    check = fields.Char(string="Check")

class SrockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    name= fields.Char('Name')