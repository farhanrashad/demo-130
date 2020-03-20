# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrOvertime(models.Model):
    _inherit = 'hr.employee'

    @api.depends('entry_checklist')
    def compute_entry_checklist_progress(self):
        for rec in self:
            total_len = self.env['hr.employee.entry.checklist'].search_count([])
            check_list_len = len(rec.entry_checklist)
            if total_len != 0:
                rec.entry_checklist_progress = (check_list_len * 100) / total_len

    @api.depends('exit_checklist')
    def compute_exit_checklist_progress(self):
        for rec in self:
            total_len = self.env['hr.employee.exit.checklist'].search_count([])
            check_list_len = len(rec.exit_checklist)
            if total_len != 0:
                rec.exit_checklist_progress = (check_list_len * 100) / total_len

    @api.constrains('entry_checklist_progress')
    def entry_progress_constraint(self):
        for rec in self:
            if rec.entry_checklist_progress < 50.0:
                raise ValidationError(_('Progress Must be more than 50 %'))

    @api.constrains('exit_checklist_progress')
    def exit_progress_constraint(self):
        for rec in self:
            if rec.exit_checklist_progress < 50.0:
                raise ValidationError(_('Progress Must be more than 50 %'))

    entry_checklist = fields.Many2many('hr.employee.entry.checklist')
    entry_checklist_progress = fields.Float(string='Progress', compute='compute_entry_checklist_progress', store=True,
                                            recompute=True, default=0.0)
    exit_checklist = fields.Many2many('hr.employee.exit.checklist')
    exit_checklist_progress = fields.Float(string='Progress', compute='compute_exit_checklist_progress', store=True,
                                           recompute=True, default=0.0)


class HrEntryChecklist(models.Model):
    _name = 'hr.employee.entry.checklist'
    _description = 'Employee Entry Checklist'
    _rec_name = 'entry_name'

    entry_name = fields.Char(string='Name', required=True)
    desc = fields.Char(string='Description')


class HrExitChecklist(models.Model):
    _name = 'hr.employee.exit.checklist'
    _description = 'Employee Exit Checklist'
    _rec_name = 'exit_name'

    exit_name = fields.Char(string='Name', required=True)
    desc = fields.Char(string='description')
