# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
from datetime import datetime


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
            
            move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
            vals = {
                'partner_id': self.bom_id.subcontractor_ids.id,
                'date_order': fields.Date.today(),
            }
            order = self.env['purchase.order'].create(vals)
            
            for order_line in self.move_raw_ids:
                values = {
                'order_id' : order.id,
                'product_id': order_line.product_id.id,
                'name' : order_line.product_id.name,
                'product_qty': order_line.product_uom_qty,
                'price_unit':order_line.product_id.standard_price,
                'date_planned': fields.Date.today(),
                'product_uom': order_line.product_id.uom_po_id.id, 
            }
            purchse_order_line = self.env['purchase.order.line'].create(values)

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
                move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
                vals = {
                    'partner_id': self.bom_id.subcontractor_ids.id,
                    'date_order': fields.Date.today(),
                }
                order = self.env['purchase.order'].create(vals)
                
                for order_line in self.move_raw_ids:
                    values = {
                    'order_id' : order.id,
                    'product_id': order_line.product_id.id,
                    'name' : order_line.product_id.name,
                    'product_qty': order_line.product_uom_qty,
                    'price_unit':order_line.product_id.standard_price,
                    'date_planned': fields.Date.today(),
                    'product_uom': order_line.product_id.uom_po_id.id, 
                }
                purchse_order_line = self.env['purchase.order.line'].create(values)

    def production_count(self):
        record = self.env['mrp.production'].search_count([('product_id', '=', self.product_id.id)])
        self.production_order_count = record

    def purchase_count(self):
        record = self.env['purchase.order'].search_count([('partner_id', '=', self.bom_id.subcontractor_ids.id)])
        self.purchase_order_count = record
        