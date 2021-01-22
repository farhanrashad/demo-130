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
            'name': 'All PO',
            'view_id': self.env.ref('purchase.purchase_order_tree', False).id,
            'target': 'new',
            'res_model': 'purchase.order',
            'view_mode': 'tree',
        }

    def purchase_revision(self):
        self.rev_po_name = 'REV-' + self.name
        self.revision_user = self.env.user.name
        # line_ids=[]
        # for line in self.order_line:
        #     order_line = {
        #         'order_id': self.id,
        #         'product_id': line.product_id.id,
        #         'name': line.name,
        #         'product_qty': line.product_qty,
        #         'price_unit_dup': line.price_unit_dup,
        #         'price_subtotal': line.price_subtotal,
        #         'price_unit': line.price_unit_dup
        #     }
        #     line_ids.append(order_line)
        # vals = {
        #     'partner_id': self.partner_id.id,
        #     'date_approve': fields.Date.today(),
        #     'partner_ref': self.partner_ref,
        #     'company_id': self.env.company.id,
        #     'order_line': line_ids
        # }
        # order = self.env['purchase.order'].create(vals)
            # orders_lines = self.env['purchase.order.line'].create(order_line)

        line_vals = []
        for line in self.order_line:
            line_vals.append((0, 0, {
                'order_id': self.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_qty': line.product_qty,
                'price_unit_dup': line.price_unit_dup,
                'price_subtotal': line.price_subtotal,
                'price_unit': line.price_unit_dup
            }))
            line_vals.append(line_vals)
        vals = {
            'partner_id': self.partner_id.id,
            'date_approve': fields.Date.today(),
            'partner_ref': self.partner_ref,
            'company_id': self.env.company.id,
            'order_line': line_vals
        }
        move = self.env['purchase.order'].create(vals)