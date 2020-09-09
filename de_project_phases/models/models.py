# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectStages(models.Model):
    _name = 'project.phases'
    _description = 'This is Project Phases'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(String="Name", store=True ,required=True)
    project_id = fields.Many2one('project.project', string='Project')
    sequence = fields.Integer(string='Sequence')
    start_date = fields.Date(string='Start Date', store=True)
    end_date = fields.Date(string='End Date', store=True)
    user_id = fields.Many2one('res.users', string='Responsible User', store='True')
    company_id = fields.Many2one('res.company', string='Company',)
    note = fields.Text()
    
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
