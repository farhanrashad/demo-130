# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import fields,models

class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_configs = fields.Many2many('pos.config', string='Default Point of Sale', domain=[('active', '=', True)])


    def write(self, vals):
    	if 'pos_configs' in vals:
    		self.env['ir.rule'].clear_caches()
    	return super(ResUsers, self).write(vals)
