# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    task_progress_restriction = fields.Selection([('no_restriction ', 'No Restriction To Task Progress'),
                                                  ('restrict', 'Restrict Task Progress Before All Checklist Completion')],
                                                 string='Task Progress Restriction')


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    checklist_task_progress_restriction = fields.Boolean(string='Checklist Task Progress Restriction')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_checklist_id = fields.Many2one('project.checklist.task.checklist', string='Checklist')
    checklist_item_ids = fields.One2many('project.checklist.items', 'project_task_id', string='Checklist Items')
