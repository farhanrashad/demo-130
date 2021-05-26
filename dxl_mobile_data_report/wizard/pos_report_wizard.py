# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MobileDataReportWizard(models.TransientModel):
    _name = 'mobile.data.report.wizard'
    _description = 'Mobile Data report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    shop_ids = fields.Many2many('pos.multi.shop', string="Shop", required=True)

    def print_mobile_data_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'shop_ids': self.shop_ids.ids,
        }
        return self.env.ref('dxl_mobile_data_report.mobile_data_xlsx').report_action(self, data=data)
