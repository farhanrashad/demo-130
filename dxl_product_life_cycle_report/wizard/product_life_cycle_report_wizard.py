# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductLifeCycleReportWizard(models.TransientModel):
    _name = 'product.life.cycle.report.wizard'
    _description = 'Product Life Cycle report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    category_ids = fields.Many2many('product.category', string="Product Category")
    product_ids = fields.Many2many('product.product', string="Product")

    @api.onchange('category_ids')
    def _onchange_amount(self):
        if self.category_ids:
            return {'domain': {'product_ids': [('categ_id', 'in', self.category_ids.ids)]}}
        return {}

    def print_product_life_cycle_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'category_ids': self.category_ids.ids,
            'product_ids': self.product_ids.ids,
        }
        self.category_ids = False
        self.product_ids = False
        return self.env.ref('dxl_product_life_cycle_report.product_life_cycle_xlsx').report_action(self, data=data)
