# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class pos_config(models.Model):
    _inherit = 'pos.config' 

    allow_orderline_user = fields.Boolean('Allow Orderline User', default=True)

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    user_id = fields.Many2one("hr.employee", "Salesperson")
