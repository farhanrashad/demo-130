# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    purchase_demand_id = fields.Many2one('purchase.demand', string='Purchase Requistion', copy=False)
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
   
    purchase_demand_line_id = fields.Many2one('purchase.demand.line', readonly=True)
