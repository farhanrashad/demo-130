# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    ticket_id = fields.Many2one('helpdesk.ticket', string="Ticket", help="Related Helpdesk Ticket")
    is_diagnosys = fields.Boolean('Is Diagnosys')
    is_workorder = fields.Boolean('Is Workorder')
    
    repair_planning_lines = fields.One2many('project.task.planning.line', 'task_id', string='Task Repair Planning Lines', readonly=False, copy=True, auto_join=True)

    sale_count = fields.Integer('sale Count', compute='_compute_sale_count', compute_sudo=True)
    sale_ids = fields.One2many('sale.order', 'task_id', string='Quotation')
    
class ProjectTaskRepairPlanning(models.Model):
    _name = 'project.task.planning.line'
    _description = 'Repair Planning Line'
    _order = 'id desc'
    
    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id
    
    task_id = fields.Many2one('project.task', string='Task', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True,)
    product_uom_qty = fields.Float('Quantity', default=1.0, required=True)
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_product_uom_id, required=True,
        help="Unit of Measure (Unit of Measure) is the unit of measurement for the inventory control", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')