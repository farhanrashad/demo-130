# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ShopWiseProfitWizard(models.TransientModel):
    _name = 'shop.wise.profit.wizard'
    _description = 'Shop Wise Profit Wizard'

    start_at = fields.Datetime(string='From Date', required=True)
    stop_at = fields.Datetime(string="To Date", required=True)
    region_ids = fields.Many2many('analytic.region', string="Region", required=True)
    analytic_account_ids = fields.Many2many('account.analytic.account', string="Locations", required=True)

    def shop_wise_profit_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'analytic_account_ids': self.analytic_account_ids.ids,
            'region_ids': self.region_ids.ids,
        }
        return self.env.ref('shop_wise_profit.pos_xlsx').report_action(self, data=data)

    @api.onchange('region_ids')
    def onchange_region_ids(self):
        self.analytic_account_ids = False
