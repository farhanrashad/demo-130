# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _inherit = 'hr.employee'
    
    kra_total_score = fields.Float(compute='_compute_kra_data', string="Score", help="Total Score of KRA", )
    kra_line_ids = fields.One2many('hr.employee.kra.line', 'employee_id', string='Orders')
    
    @api.depends('kra_line_ids.score')
    def _compute_kra_data(self):
        for kra in self:
            total = 0.0
            for line in kra.kra_line_ids:
                total += line.score
            kra.kra_total_score = total
            
    def action_view_employee_kra_line(self):
        action = self.env.ref('employee_kra_entries_action').read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        orders = self.mapped('kra_line_ids')
        if len(orders) == 1:
            action['views'] = [(self.env.ref('employee_kra_form_view').id, 'form')]
            action['res_id'] = orders.id
        return action