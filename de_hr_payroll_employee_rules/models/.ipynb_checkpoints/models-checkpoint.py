# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
class HrContract(models.Model):
    _inherit = 'hr.contract'

    structure_lines = fields.One2many('hr.payroll.structure.line', string='Structure Lines')


class HrPayrollStructureExt(models.Model):
    _inherit = 'hr.payroll.structure.type'
#     _description = 'This is Structure Lines'

    structure_lines = fields.One2many('hr.payroll.structure.line', string='Structure Lines')


class HrPayrollStructureLine(models.Model):
    _name = 'hr.payroll.structure.line'
    _description = 'This is Structure Lines'

    name = fields.Many2one('hr.payroll.input.type', string='Description')
    struct_id = fields.Many2one('hr.payroll.structure.type', string='Structure')
#     value = fields.Integer()
    amount = fields.Float(string='Amount', store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
