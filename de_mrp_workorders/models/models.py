# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
   
    routing_f_id = fields.Many2one(
        'mrp.routing', srting='Routing')
    routing_s_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    routing_t_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    routing_fo_id = fields.Many2one(
        'mrp.routing', string='Routing', store=True)
    product_f_qty = fields.Float(string='Quantity To Produce')
    product_s_qty = fields.Float(string='Quantity To Produce')
    product_t_qty = fields.Float(string='Quantity To Produce')
    product_fo_qty = fields.Float(string='Quantity To Produce')
    
    def button_plan(self):
        """ Create work orders. And probably do stuff, like things. """
        if routing_f_id != '':
            orders_to_plan = self.filtered(lambda order: order.routing_f_id)
            for order in orders_to_plan:
                order.move_raw_ids.filtered(lambda m: m.state == 'draft')._action_confirm()
                quantity = order.product_uom_id._compute_quantity(order.product_f_qty, order.bom_id.product_uom_id) / order.bom_id.product_qty
                boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
                order._generate_workorders(boms)
                order._plan_workorders()
        elif routing_s_id != '':
            orders_to_plan = self.filtered(lambda order: order.routing_s_id)
            for order in orders_to_plan:
                order.move_raw_ids.filtered(lambda m: m.state == 'draft')._action_confirm()
                quantity = order.product_uom_id._compute_quantity(order.product_s_qty, order.bom_id.product_uom_id) / order.bom_id.product_qty
                boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
                order._generate_workorders(boms)
                order._plan_workorders()
        elif routing_t_id != '':
            orders_to_plan = self.filtered(lambda order: order.routing_t_id)
            for order in orders_to_plan:
                order.move_raw_ids.filtered(lambda m: m.state == 'draft')._action_confirm()
                quantity = order.product_uom_id._compute_quantity(order.product_t_qty, order.bom_id.product_uom_id) / order.bom_id.product_qty
                boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
                order._generate_workorders(boms)
                order._plan_workorders()
        if routing_fo_id != '':
            orders_to_plan = self.filtered(lambda order: order.routing_fo_id)
            for order in orders_to_plan:
                order.move_raw_ids.filtered(lambda m: m.state == 'draft')._action_confirm()
                quantity = order.product_uom_id._compute_quantity(order.product_fo_qty, order.bom_id.product_uom_id) / order.bom_id.product_qty
                boms, lines = order.bom_id.explode(order.product_id, quantity, picking_type=order.bom_id.picking_type_id)
                order._generate_workorders(boms)
                order._plan_workorders()        
        return True