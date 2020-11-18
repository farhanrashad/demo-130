# -- coding: utf-8 --
import datetime
from odoo import api, fields, models, _
from odoo.tools import float_compare
from odoo.exceptions import UserError, ValidationError, Warning

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_type = fields.Many2one(string="Property Type")
    uom_id = fields.Many2one("uom.uom" ,string="UOM")
    property_location = fields.Char(string="Property Location")
    property_area = fields.Float(string="Property Area")

    owner_address = fields.Char(string="Owner")
    owner_email = fields.Char(string="Email")
    owner_phone = fields.Char(string="Phone")


