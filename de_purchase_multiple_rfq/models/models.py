# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from collections import defaultdict
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime , timedelta




class PurchaseOrderMultiple(models.Model):
    _name = 'purchase.order.multiple'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Multiple Purchase Order'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.multiple') or 'New'
        result = super(PurchaseOrderMultiple, self).create(vals)
        return result

    

    

    def action_generate_po(self):
        vendor_list = []
        for line in self.sheet_ids:
            vendor_list.append(line.vendor_id)
        list = set(vendor_list)
        for te in list:
            product = []
            for re in self.sheet_ids:
                if te == re.vendor_id:
                    valss = {
                        'product_id': re.product_id.id,
                        'name': re.product_name,
                        'product_qty': re.product_quantity,
                        'analytic_tag_ids': [(6, 0, re.analytic_tag_ids.ids)],
                        'price_unit': re.product_id.standard_price,
                        'date_planned': fields.Date.today(),
                        'product_uom': re.uom_id.id,
                    }
                    product.append(valss)
            vals = {
                  'partner_id': te.id,
                  'date_order': fields.Date.today(),
                  'origin': self.name,
                    }
            order = self.env['purchase.order'].create(vals)
            for test in product:
                order_line = {
                       'order_id': order.id,
                       'product_id': test['product_id'],
                       'name': test['name'],
                       'product_qty': test['product_qty'],
                       'analytic_tag_ids': test['analytic_tag_ids'],
                       'price_unit': test['price_unit'],
                       'date_planned': fields.Date.today(),
                       'product_uom': test['product_uom'],
                        }
                orders_lines = self.env['purchase.order.line'].create(order_line)
                self.write({
                    'po_created': True
                })


    name = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    
    date = fields.Date(string='Date', store=True, default=str(datetime.today()))
    po_created = fields.Boolean(string='PO Created')
    manual_input = fields.Char(string='Manual Demand #:', store=True, required=True)
    sheet_ids = fields.One2many(comodel_name='purchase.order.multiple.line', inverse_name='sheet_id')


class JobOrderSheetLine(models.Model):
    _name = 'purchase.order.multiple.line'
    _description = 'Material Planning'



    sheet_id = fields.Many2one(comodel_name='purchase.order.multiple')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    product_name = fields.Char(string='Product Name', related='product_id.name')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    product_quantity = fields.Float(string='Quantity')
    uom_id = fields.Many2one('uom.uom',string='Unit of Measure',related='product_id.uom_po_id')
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor', required=True)
