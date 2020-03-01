# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class Construction(models.Model):
#     _name = 'construction.construction'
#     _description = 'this is construction model'
#
#     name = fields.Char(string='Name')

class Projectcons(models.Model):
    _name = 'projects.projects'
    _description = 'this is project model'

    def action_share(self):
        print('world')

    # ('class_student', '=', self.id)
    def get_document_count(self):
        count = self.env['projects.projects'].search_count([])
        self.documents_count = count

    def get_task_count(self):
        count = self.env['projects.projects'].search_count([])
        self.task_count = count

    def get_notes_count(self):
        count = self.env['projects.projects'].search_count([])
        self.notes_count = count

    # @api.depends('visibility')
    # def set_default_value(self):
    #     for i in self:
    #         i.visibility = 'All employees'

    name = fields.Char(string='Name', bold=True)
    task_name = fields.Char(string='Name of tasks:')
    # projects_projects_linea = fields.One2many('projects.projects.linea', 'sub_task_project', string='settings')
    documents_count = fields.Integer(compute='get_document_count')
    task_count = fields.Integer(compute='get_task_count')
    notes_count = fields.Integer(compute='get_notes_count')

    project_manager = fields.Many2one('res.users', string='Project Manager')
    customer_name = fields.Many2one('res.partner', string='customer')
    # analytic_account = fields.
    visibility = fields.Char(string='Visibility', default='All employees')
    sub_task_project = fields.Many2one('projects.projects', string='Sub-task Project')
    company = fields.Many2one('res.company', string='Company')


class Projectlineitem(models.Model):
    _name = 'projects.projects.linea'
    _description = 'this is project line table'




class Projectcons(models.Model):
    _name = 'notes.notes'
    _description = 'this is project model'
    _rec_name = 'tes_note'

    tags_note = fields.Char(string='Tags')
    task_job_order = fields.Many2one('order.job',string='Task/ Job Order')
    construction_projecct = fields.Many2one('projects.projects',string='Construction Project')
    responsible_user = fields.Many2one('res.users',string='Responsible User')
    tes_note = fields.Text()


# class de_construction_app(models.Model):
#     _name = 'de_construction_app.de_construction_app'
#     _description = 'de_construction_app.de_construction_app'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
