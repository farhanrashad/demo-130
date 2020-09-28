# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

    
class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    asset_sequence = fields.Boolean(string="Asset Sequence", default=True)
    

# implied_group='de_account_asset_number.group_asset_sequence'    
#     def set_values(self):
#         super(AccountConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param("de_account_asset_number.asset_sequence",
#                                                          self.notice_period)
# #         self.env['ir.config_parameter'].sudo().set_param("de_account_asset_number.no_of_days",
# #                                                          self.no_of_days)

#     @api.model
#     def get_values(self):
#         res = super(AccountConfigSettings, self).get_values()
#         get_param = self.env['ir.config_parameter'].sudo().get_param
#         res['asset_sequence'] = get_param('de_account_asset_number.asset_sequence')
# #         res['no_of_days'] = int(get_param('de_account_asset_number.no_of_days'))
#         return res