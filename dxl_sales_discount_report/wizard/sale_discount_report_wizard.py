# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleDiscountReportWizard(models.TransientModel):
    _name = 'sale.discount.report.wizard'
    _description = 'Sale Discount report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    shop_ids = fields.Many2many('pos.multi.shop', string="Shop", required=True)

    def print_sale_discount_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'shop_ids': self.shop_ids.ids,
        }
        return self.env.ref('dxl_sales_discount_report.sale_discount_xlsx').report_action(self, data=data)
