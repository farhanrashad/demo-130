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
#             'multi': False,
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
#             'multi': False,
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
#             vals['move_raw_ids'] = line_ids
#             raise UserError(_(line_ids))
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
            if record.bom_id.type=='normal':
                vals = {
                    'product_id': record.product_id.id,
                    'product_qty': record.product_qty,
                    'bom_id': record.bom_id.id,
                    'date_planned_start': record.date_planned_start,
                    'company_id': record.company_id.id,
                    'product_uom_id': record.product_id.uom_id.id,
                }
                order = self.env['mrp.production'].create(vals)

            if record.bom_id.type=='subcontract':
                move = self.env['mrp.bom'].search([('product_tmpl_id','=', self.bom_id.id)])
                vals = {
                    'origin': self.origin,
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
            
#         record = self.env['mrp.production'].search_count([('product_id', '=', self.product_id.id)])
#         self.production_order_count = record

    def purchase_count(self):
        for record in self:
            record.purchase_order_count = self.env['purchase.order'].search_count([('origin','=',record.name)])
            
#         record = self.env['purchase.order'].search_count([('partner_id', '=', self.bom_id.subcontractor_ids.id)])
#         self.purchase_order_count = record

# def semi_finish_order(self):
#         for line in self:
#             if line.production_created == False and line.type == 'normal':
#                 bom_qty = 0.0
#                 line_bom = self.env['mrp.bom'].search([('product_tmpl_id.name','=',line.product_id.name)])
#                 for bom in line_bom:
#                     line__bom_vals = []
#                     for component in bom.bom_line_ids:
#                         line__bom_vals.append((0,0, {
#                                 'product_id': component.product_id.id,
#                                 'name': component.product_id.name,
#                                 'product_uom': component.product_id.uom_po_id.id,
#                                 'product_uom_qty': component.product_qty,
#                                 'date': fields.Date.today(),
#                                 'date_expected': fields.Date.today(),
#                                 'location_id': line.location_src_id.id,
#                                 'location_dest_id': line.location_dest_id.id,
#                         }))
#                 production_vals ={
#                         'product_id': line.product_id.id,
#                         'product_uom_id': line.product_id.uom_id.id,
#                         'product_qty': line.production_quantity,
#                         'origin': self.job_order_id.name, 
#                         'job_order_id': self.job_order_id.id, 
#                         'bom_id': line_bom[0].id,
#                         'date_planned_start': fields.Date.today(),
#                         'picking_type_id': line.picking_type_id.id,
#                         'location_src_id': line.location_src_id.id,
#                         'location_dest_id': line.location_dest_id.id,
#                         'move_raw_ids': line__bom_vals ,
#                 }
#                 production_order = self.env['mrp.production'].create(production_vals)
#                 if line.production_created == False and line.type == 'normal':
#                     line.update ({
# #                    'po_process': False,
#                         'production_created': True,
#                         })
















#     def action_generate_production_order(self):
#         production_list = []
#         for production_order in self:             
#             product_quantity = 0.0              
#             for bom_production in self:
#                 if production_order.bom_id == bom_production.bom_id:
#                     product_quantity = product_quantity + bom_production.product_qty
#             valss = {
#                     'product_id': production_order.product_id.id,
#                     'product_uom_id': production_order.product_id.uom_id.id,
#                     'product_qty': product_quantity,
#                     'origin': production_order.name, 
#                     'bom_id': production_order.bom_id.id,
#                     'date_planned_start': fields.Date.today(),
#                     'picking_type_id': production_order.picking_type_id.id,
#                     'location_src_id': production_order.location_src_id.id,
#                     'location_dest_id': production_order.location_dest_id.id,
#                 }  
#             production_list.append(valss)
#             # seperate loop
#         for order in  production_list: 
#             production_vals ={
#                 'product_id': order['product_id'],
#                 'product_uom_id': order['product_uom_id'],
#                 'product_qty': order['product_qty'],
#                 'origin': order['origin'],  
#                 'bom_id': order['bom_id'],
#                 'date_planned_start': fields.Date.today(),
#                 'picking_type_id': order['picking_type_id'],
#                 'location_src_id': order['location_src_id'],
#                 'location_dest_id': order['location_dest_id'],
#             }
#             production_order = self.env['mrp.production'].create(production_vals)