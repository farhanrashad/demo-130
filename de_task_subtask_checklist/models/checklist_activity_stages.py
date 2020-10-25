# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ChecklistActivityStages(models.Model):
    _name = 'project.checklist.activity.stages'
    _description = 'Checklist Activity Stages'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence')
    default_stage = fields.Many2one('project.task.type', string='Default Stage')


class TaskChecklist(models.Model):
    _name = 'project.checklist.task.checklist'
    _description = 'Tasks Checklist'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    checklist_item_ids = fields.One2many('project.checklist.items', 'task_checklist_id', string='Checklist Items')


class ChecklistItems(models.Model):
    _name = 'project.checklist.items'
    _description = 'Checklist Items'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    task_checklist_id = fields.Many2one('project.checklist.task.checklist', string='Task Checklist')
    project_task_id = fields.Many2one('project.task', string='Project Tasks')


class ProjectChecklistLine(models.Model):
    _name = 'project.checklist.line'
    _description = 'Project Checklist Line'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')