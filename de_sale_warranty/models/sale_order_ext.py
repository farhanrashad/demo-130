# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
import dateutil.parser
from odoo.exceptions import UserError, ValidationError, Warning
from dateutil.relativedelta import relativedelta


class StockPickingExt(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
        b = str(sale_order.date_order)
        date = dateutil.parser.parse(b).date()
        for line in sale_order.order_line:
            interval_type = line.product_id.warranty_period
            interval_amount = line.product_id.warranty_period_interval
            if interval_type == 'd':
                new_date = date + datetime.timedelta(days=interval_amount)
            elif interval_type == 'm':
                new_date = date + relativedelta(months=3)
            elif interval_type == 'y':
                new_date = date + relativedelta(years=1)
            else:
                raise UserError(_("Please check warranty interval."))

            if line.product_id.is_warranty == True:
                self.env['sales.warranty'].create({
                    'partner_id': sale_order.partner_id.id,
                    'type': line.product_id.warranty_type.id,
                    'product_id': line.product_id.id,
                    'purchase_date': date,
                    'warranty_start_date': date,
                    'warranty_end_date': new_date,
                    'company_id': self.env.company.id,
                    'sale_id': sale_order.id,
                })
        res = super(StockPickingExt, self).button_validate()
        return res


class SaleOrderWarranty(models.Model):
    _inherit = 'sale.order'

    def get_warranty_doc_count(self):
        count = self.env['sales.warranty'].search_count([('sale_id', '=', self.id)])
        self.warranty_docs = count

    def action_warranty_docs(self):
        self.ensure_one()
        return {
            'name': 'Sale Warranty',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sales.warranty',
            'domain': [('sale_id', '=', self.id)],
        }

    def action_warranty_renew(self):
        warranty_docs = self.env['sales.warranty'].search([('sale_id', '=', self.id)])
        for doc in warranty_docs:
            if doc.warranty_end_date <= fields.Date.today():
                self.env['sales.warranty'].create({
                    'partner_id': doc.partner_id.id,
                    'type': doc.type.id,
                    'product_id': doc.product_id.id,
                    'purchase_date': doc.purchase_date,
                    'warranty_start_date': fields.Date.today(),
                    'warranty_end_date': doc.warranty_end_date,
                    'company_id': self.env.company.id,
                    'sale_id': doc.sale_id.id,
                    'ref_warranty': doc.name,
                })

    def action_warranty_expire(self):
        print('expire')
        warranty_expire = self.env['sales.warranty'].search([])
        for expire in warranty_expire:
            if expire.warranty_end_date <= fields.Date.today():
                expire.update({
                    'state': 'expired'
                })

    warranty_docs = fields.Integer(string='Warranty', compute='get_warranty_doc_count')


class ProductProductExt(models.Model):
    _inherit = 'product.product'

    def action_warranty_docs(self):
        self.ensure_one()
        return {
            'name': 'Product Warranty',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sales.warranty',
            'domain': [('product_id', '=', self.id)],
        }

    def get_warranty_doc_count(self):
        count = self.env['sales.warranty'].search_count([('product_id', '=', self.id)])
        self.warranty_docs = count

    warranty_docs = fields.Integer(string='Warranty', compute='get_warranty_doc_count')


class ResPartnerWarranty(models.Model):
    _inherit = 'res.partner'

    def action_warranty_docs(self):
        self.ensure_one()
        return {
            'name': 'Customer Warranty',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sales.warranty',
            'domain': [('partner_id', '=', self.id)],
        }

    def get_warranty_doc_count(self):
        count = self.env['sales.warranty'].search_count([('partner_id', '=', self.id)])
        self.warranty_docs = count

    warranty_docs = fields.Integer(string='Warranty', compute='get_warranty_doc_count')
