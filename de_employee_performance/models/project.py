# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_kra_line = fields.One2many('hr.employee.kra.line', 'task_id', string='Task Kra Lines', )
    kra_total_score = fields.Float(compute='_compute_kra_score_total', string='Total Score', readonly=True, store=True)

    @api.depends('task_kra_line.score')
    def _compute_kra_score_total(self):
        """
        Compute the KRA Total of line.
        """
        for task in self:
            total_score = 0.0
            for line in task.task_kra_line:
                total_score += line.score
            task.update({
                'kra_total_score': total_score,
            })

            
class EmpoyeeKraLine(models.Model):
    _name = 'hr.employee.kra.line'
    _description = 'Task KRA Line'
    
    task_id = fields.Many2one('project.task', string='Task Reference', required=False, ondelete='cascade', index=True, copy=False)
    kra_id = fields.Many2one('hr.kra', string='Kra', required=True, change_default=True, ondelete='restrict')
    kra_line_id = fields.Many2one('hr.kra.line', required=False, string='Result', domain="[('kra_id', '=', kra_id)]", change_default=True, ondelete='restrict')
    score = fields.Float(related='kra_line_id.score', string='Score', store=True,readonly=True)
    name = fields.Char(string='Description')
    employee_id = fields.Many2one('hr.employee', "Employee", compute='_get_employee', required=True, readonly=False, store=True,)
    manager_id = fields.Many2one('res.users', string='Manager', index=True, tracking=2, readonly=True, default=lambda self: self.env.user,)
    kra_date = fields.Date(string='Date', required=True, readonly=True, index=True, copy=False, default=fields.Date.today(), )

    
    @api.depends('task_id','kra_id','task_id.user_id')
    def _get_employee(self):
        for line in self:
            line.update({
                'employee_id': line.task_id.user_id.employee_id.id,
            })
    
    
    