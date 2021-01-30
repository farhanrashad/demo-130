# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    default_warranty_policy = fields.Selection([
        ('order', 'Warranty start on order confirmation'),
        ('delivery', 'Warranty start on delivery')
        ], 'Warranty Policy',
        default='order',
        default_model='product.template')
    
    default_warranty_period = fields.Selection([
        ('d', 'Day(s)'),
        ('m', 'Month(s)'),
        ('y', 'Year(s)'),
        ], 'Warranty period',
        default='d',
        default_model='product.template')
    
    warranty_period_interval = fields.Integer(related='company_id.warranty_period_interval', required=True, readonly=False)
    
    
    
#     def set_values(self):
#         res = super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].set_param('de_sale_warranty.warranty_period_interval', self.warranty_period_interval)
#         self.env['ir.config_parameter'].set_param('de_sale_warranty.default_warranty_period', self.default_warranty_period)
#         self.env['ir.config_parameter'].set_param('de_sale_warranty.default_warranty_policy ', self.default_warranty_policy )
# 
#         return res
# 
#     def get_values(self):
#         res = super(ResConfigSettings, self).get_values()
#         ICPSudo = self.env['ir.config_parameter'].sudo()
#         stock = ICPSudo.get_param('de_sale_warranty.warranty_period_interval')
#         stocks = ICPSudo.get_param('de_sale_warranty.default_warranty_period')
#         stockss = ICPSudo.get_param('de_sale_warranty.default_warranty_policy')
# 
# 
#         res.update(
#             warranty_period_interval = stock,
#             default_warranty_period = stocks,
#             default_warranty_policy = stockss,
#             
#         )
#         return res
    