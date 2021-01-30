# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class PurchaseOrder(models.Model):
    _inherit = 'res.partner'
    
    order_category = fields.Char(string='Order Category')
    
    