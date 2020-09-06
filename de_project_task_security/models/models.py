# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_project_task_security(models.Model):
#     _name = 'de_project_task_security.de_project_task_security'
#     _description = 'de_project_task_security.de_project_task_security'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
