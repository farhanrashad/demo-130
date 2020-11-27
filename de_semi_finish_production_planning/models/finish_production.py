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
                'product_uom_id': self.product_id.uom_id.id,
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

    def action_generate_production_order(self):
        production_list = []
        for production_order in self:             
            product_quantity = 0.0              
            for bom_production in self:
                if production_order.bom_id == bom_production.bom_id:
                    product_quantity = product_quantity + bom_production.product_qty
            valss = {
                    'product_id': production_order.product_id.id,
                    'product_uom_id': production_order.product_id.uom_id.id,
                    'product_qty': product_quantity,
                    'origin': production_order.name, 
                    'bom_id': production_order.bom_id.id,
                    'date_planned_start': fields.Date.today(),
                    'picking_type_id': production_order.picking_type_id.id,
                    'location_src_id': production_order.location_src_id.id,
                    'location_dest_id': production_order.location_dest_id.id,
                }  
            production_list.append(valss)
            # seperate loop
        for order in  production_list: 
            production_vals ={
                'product_id': order['product_id'],
                'product_uom_id': order['product_uom_id'],
                'product_qty': order['product_qty'],
                'origin': order['origin'],  
                'bom_id': order['bom_id'],
                'date_planned_start': fields.Date.today(),
                'picking_type_id': order['picking_type_id'],
                'location_src_id': order['location_src_id'],
                'location_dest_id': order['location_dest_id'],
            }
            production_order = self.env['mrp.production'].create(production_vals)
            
#         for record in self:
#             if record.bom_id.type=='normal':
#                 vals = {
#                     'product_id': record.product_id.id,
#                     'product_qty': record.product_qty,
#                     'bom_id': record.bom_id.id,
#                     'date_planned_start': record.date_planned_start,
#                     'company_id': record.company_id.id,
#                     'product_uom_id': record.product_id.uom_id.id,
#                 }
#                 order = self.env['mrp.production'].create(vals)
                
#                 for move_raw_ids in self.move_raw_ids:
#                     values = {
#                     'order_id' : order.id,
#                     'product_id': order_line.product_id.id,
#                     'name' : order_line.product_id.name,
#                     'product_qty': order_line.product_uom_qty,
#                     'price_unit':order_line.product_id.standard_price,
#                     'date_planned': fields.Date.today(),
#                     'product_uom': order_line.product_id.uom_po_id.id, 
#                 }
#                 stock_move = self.env['stock.move'].create(values)

#             if record.bom_id.type=='subcontract':
#                 move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
#                 vals = {
#                     'partner_id': self.bom_id.subcontractor_ids.id,
#                     'date_order': fields.Date.today(),
#                 }
#                 order = self.env['purchase.order'].create(vals)
                
#                 for order_line in self.move_raw_ids:
#                     values = {
#                     'order_id' : order.id,
#                     'product_id': order_line.product_id.id,
#                     'name' : order_line.product_id.name,
#                     'product_qty': order_line.product_uom_qty,
#                     'price_unit':order_line.product_id.standard_price,
#                     'date_planned': fields.Date.today(),
#                     'product_uom': order_line.product_id.uom_po_id.id, 
#                 }
#                 purchse_order_line = self.env['purchase.order.line'].create(values)

    def production_count(self):
        record = self.env['mrp.production'].search_count([('product_id', '=', self.product_id.id)])
        self.production_order_count = record

    def purchase_count(self):
        record = self.env['purchase.order'].search_count([('partner_id', '=', self.bom_id.subcontractor_ids.id)])
        self.purchase_order_count = record