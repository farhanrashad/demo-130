# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from datetime import datetime
from datetime import date

class ProjectTaskInherit(models.Model):
    _inherit = 'purchase.order'
    _description = 'This table handle the data of revision of purchase order'

    rev_po_name = fields.Char(string='Name')
    revision_user = fields.Char(string='Revision User')
    po_rev_count = fields.Integer(string='PO Revisions')

    def action_purchase_revision(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'view_id': self.env.ref('purchase.purchase_order_tree', False).id,
            'target': 'new',
            'res_model': 'purchase.order',
            'view_mode': 'tree',
        }

    def purchase_revision(self):
        self.rev_po_name = 'REV-' + self.name
        self.revision_user = self.env.user.name
    
        line_vals = []
        for line in self.order_line:
            purchase = {
                'product_id': line.product_id.id,
#                 'account_id': self.partner_id.property_account_payable_id.id,
                'name': line.name,
                'analytic_tag_ids': line.analytic_tag_ids.id,
                'account_analytic_id': line.account_analytic_id.id,
                'product_qty': line.product_qty,
                'price_unit': line.price_unit,
                'date_planned': line.date_planned,
                'product_uom': line.product_uom.id,
                'price_subtotal': line.price_subtotal,
            }
            line_vals.append(purchase)
        
        vals = {
            'partner_id': self.partner_id.id,
            'company_id': self.env.company.id,
        }
        move = self.env['purchase.order'].create(vals)
        for purchase_line in line_vals:
            purchase_line_vals = {
                'order_id': move.id,
                 'product_id': purchase_line['product_id'],
#                 'account_id': self.partner_id.property_account_payable_id.id,
                'name': purchase_line['product_id'],
                'analytic_tag_ids': purchase_line['analytic_tag_ids'],
                'account_analytic_id': purchase_line['account_analytic_id'],
                'product_qty': purchase_line['product_qty'],
                'date_planned': purchase_line['date_planned'],
                'product_uom': purchase_line['product_uom'], 
                'price_unit': purchase_line['price_unit'],
                'price_subtotal': purchase_line['price_subtotal'],
            }
            purchase_lines = self.env['purchase.order.line'].create(purchase_line_vals)

        
        
