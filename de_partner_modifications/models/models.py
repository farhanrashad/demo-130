# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerModifications(models.Model):
    _name = 'partner.stages'
    _description = 'This is Partner Stages'

    name = fields.Char(string='Name', store=True)
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
