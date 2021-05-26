# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleSummaryReportWizard(models.TransientModel):
    _name = 'sale.summary.report.wizard'
    _description = 'Sale Summary report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    shop_ids = fields.Many2many('pos.multi.shop', string="Shop", required=True)
    category_ids = fields.Many2many('product.category', string="Product Category")
    product_ids = fields.Many2many('product.product', string="Product")

    @api.onchange('category_ids')
    def _onchange_amount(self):
        if self.category_ids:
            return {'domain': {'product_ids': [('categ_id', 'in', self.category_ids.ids)]}}
        return {}

    def print_sale_summary_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'shop_ids': self.shop_ids.ids,
            'category_ids': self.category_ids.ids,
            'product_ids': self.product_ids.ids,
        }
        return self.env.ref('dxl_sales_summary_report.sale_summary_xlsx').report_action(self, data=data)
