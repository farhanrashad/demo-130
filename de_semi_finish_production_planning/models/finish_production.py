# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
from datetime import datetime


class FinishProduction(models.Model):
    _inherit = 'mrp.production'
    
    def action_production_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Manufacturing Order',
            'domain': [('origin','=', self.name)],
            'target': 'current',
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
        }
    def action_purchase_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Purchase Order',
            'domain': [('origin','=', self.name)],
            'target': 'current',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
        }
    
    production_order_count = fields.Integer(compute='production_count')
    purchase_order_count = fields.Integer(compute='purchase_count')
    is_order = fields.Boolean(default=False)
                    
    def semi_finish_order(self):
        self.is_order = True
        line_ids = []
        if self.bom_id.type=='normal':
            for line in self.bom_id.bom_line_ids:
                values = (0,0,{   
                'product_id': line.product_id.id,
                'name': line.product_id.name,    
                'product_uom_qty': line.product_qty,
                'product_uom': line.product_uom_id.id,
                'date': fields.Date.today(),
                'date_expected': fields.Date.today(),
                'location_id': self.location_src_id.id,
                'location_dest_id': self.location_dest_id.id,
            })
                line_ids.append(values)
            vals = {
                'origin': self.name,
                'product_id': self.product_id.id,
                'product_qty': self.product_qty,
                'bom_id': self.bom_id.id,
                'date_planned_start': self.date_planned_start,
                'company_id': self.company_id.id,
                'product_uom_id': self.product_id.uom_id.id,
                'move_raw_ids' : line_ids,
            }    
            order = self.env['mrp.production'].create(vals)
            
            
        if self.bom_id.type=='subcontract':
            
            move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
            vals = {
                'origin': self.name,
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
            line_ids = []
            if self.bom_id.type=='normal':
                for line in self.bom_id.bom_line_ids:
                    values = (0,0,{   
                    'product_id': line.product_id.id,
                    'name': line.product_id.name,    
                    'product_uom_qty': line.product_qty,
                    'product_uom': line.product_uom_id.id,
                    'date': fields.Date.today(),
                    'date_expected': fields.Date.today(),
                    'location_id': self.location_src_id.id,
                    'location_dest_id': self.location_dest_id.id,
                })
                    line_ids.append(values)
                vals = {
                    'origin': self.name,
                    'product_id': self.product_id.id,
                    'product_qty': self.product_qty,
                    'bom_id': self.bom_id.id,
                    'date_planned_start': self.date_planned_start,
                    'company_id': self.company_id.id,
                    'product_uom_id': self.product_id.uom_id.id,
                    'move_raw_ids' : line_ids,
                }    
                order = self.env['mrp.production'].create(vals)
            
            if self.bom_id.type=='subcontract':
            
                move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
                vals = {
                    'origin': self.name,
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
        for record in self:
            record.production_order_count = self.env['mrp.production'].search_count([('origin','=',record.name)])

    def purchase_count(self):
        for record in self:
            record.purchase_order_count = self.env['purchase.order'].search_count([('origin','=',record.name)])
            