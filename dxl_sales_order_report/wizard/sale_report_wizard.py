# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = 'Sale report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)

    def print_sale_data_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
        }
        return self.env.ref('dxl_sales_order_report.sale_data_xlsx').report_action(self, data=data)
