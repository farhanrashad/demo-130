# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockTransactionReportWizard(models.TransientModel):
    _name = 'stock.transaction.report.wizard'
    _description = 'Stock Transaction report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    shop_ids = fields.Many2many('pos.multi.shop', string='Shop', required=True)

    def print_stock_transaction_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'shop_ids': self.shop_ids.ids,
        }
        return self.env.ref('dxl_stock_transaction_report.stock_trans_xlsx').report_action(self, data=data)
