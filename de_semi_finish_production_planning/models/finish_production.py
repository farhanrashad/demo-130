# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FinishProduction(models.Model):
    _inherit = 'mrp.production'

    production_order_count = fields.Integer(compute='production_count')
    purchase_order_count = fields.Integer(compute='purchase_count')
    is_order = fields.Boolean(default=False)

    def semi_finish_order(self):
        self.is_order = True
        if self.bom_id.type=='normal':
            vals = {
                'product_id': self.product_id.id,
                'product_qty': self.product_qty,
                'bom_id': self.bom_id.id,
                'date_planned_start': self.date_planned_start,
                'company_id': self.company_id.id,
            }
            order = self.env['mrp.production'].create(vals)

        if self.bom_id.type=='subcontract':
            print('---------------------------1')
            vals = {
                'partner_id': self.user_id.id,
                'date_order': fields.Date.today(),
            }
            print('---------------------------2')
            order = self.env['purchase.order'].create(vals)
            print('---------------------------3')

    def semi_finish_order_action(self):
        for record in self:
            if record.bom_id.type=='normal':
                vals = {
                    'product_id': record.product_id.id,
                    'product_qty': record.product_qty,
                    'bom_id': record.bom_id.id,
                    'date_planned_start': record.date_planned_start,
                    'company_id': record.company_id.id,
                }
                order = self.env['mrp.production'].create(vals)

            if record.bom_id.type=='subcontract':
                print('---------------------------1')
                vals = {
                    'partner_id': record.user_id.id,
                    'date_order': fields.Date.today(),
                }
                print('---------------------------2')
                order = self.env['purchase.order'].create(vals)
                print('---------------------------3')

    def production_count(self):
        record = self.env['mrp.production'].search_count([('product_id', '=', self.product_id.id)])
        self.production_order_count = record

    def purchase_count(self):
        record = self.env['purchase.order'].search_count([('partner_id', '=', self.user_id.id)])
        self.purchase_order_count = record

            # vals = {
            #     'product_id': self.product_id.id,
            #     'product_qty': self.product_qty,
            #     'bom_id': self.bom_id.id,
            #     'date_planned_start': self.date_planned_start,
            #     'company_id': self.company_id.id,
            # }
            # order = self.env['mrp.production'].create(vals)












#     @api.onchange('last_name')
#     def get_name(self):
#         if self.last_name:
#             self.name = self.first_name + " " + self.middle_name + " " + self.last_name