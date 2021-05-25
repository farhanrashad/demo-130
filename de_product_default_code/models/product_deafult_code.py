from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    name = fields.Char(string="Name")
