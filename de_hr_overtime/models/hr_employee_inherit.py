# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrOvertime(models.Model):
    _inherit = 'hr.employee'

    def count_overtime_button(self):
        count = self.env['hr.employees.overtime'].search_count([('employee_id', 'in', [self.id])])
        self.overtime_count = count

    def open_overtime(self):
        return {
            'name': _('Overtime'),
            'domain': [('employee_id', 'in', [self.id])],
            'res_model': 'hr.employees.overtime',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    weekday_ot_rate = fields.Float(string='Weekday OT Rate')
    weekend_ot_rate = fields.Float(string='Weekend OT Rate')
    overtime_count = fields.Integer(string='Overtime', compute='count_overtime_button')


class EmployeeOvertime(models.Model):
    _name = 'hr.employees.overtime'
    _description = 'Hr Employee Overtime'
    _rec_name = 'employee_id'

    def state_approve(self):
        for rec in self:
            rec.state = 'confirm'

    def state_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.depends('based_on')
    def compute_ot_rate(self):
        for rec in self:
            if rec.based_on == 'weekday':
                rec.ot_rate = rec.ot_weekday_rate
            else:
                rec.ot_rate = rec.ot_weekend_rate

    #     @api.onchange('employee_id')
    #     def _show_employee_overtime(self):
    #         for rec in self:
    #             return{'domain':{'overtime_ids':[('name', 'in', rec.employee_id)]}}

    employee_id = fields.Many2one('hr.employee', string='Employee')
    date = fields.Date(string='Date')
    based_on = fields.Selection([('weekday', 'Weekday'), ('weekend', 'Weekend')])
    overtime = fields.Char(string='Overtime')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Approved'),
        ('done', 'Paid'),
        ('cancel', 'Cancelled'),
    ], default='draft', string='State', readonly=True, index=True)

    ot_weekday_rate = fields.Float(string='OT Weekday Rate', related='employee_id.weekday_ot_rate')
    ot_weekend_rate = fields.Float(string='OT Weekend Rate', related='employee_id.weekend_ot_rate')
    ot_rate = fields.Float(string='OT Rate', compute='compute_ot_rate')
    payslip_ids = fields.Many2one('hr.payslip', string='Payslip')

    worked_hours_id = fields.Many2one('hr.attendance', string='Worked Hours')
    ot_resource_calendar_id = fields.Many2one(related='employee_id.resource_calendar_id', string='Working Hours')
    ot_hours_per_day = fields.Float(related='ot_resource_calendar_id.hours_per_day', string='Hours per Day')


class PaySlip(models.Model):
    _inherit = 'hr.payslip'

    payslip_overtime_ids = fields.One2many('hr.payslip.overtime', 'payslip_id', string='Payslip Overtime')


class PaySlipOvertime(models.Model):
    _name = 'hr.payslip.overtime'

    payslip_id = fields.Many2one('hr.employees.overtime', string='Payslip')
    date = fields.Date(related='payslip_id.date', string='Date')
    based_on = fields.Selection(related='payslip_id.based_on', string='Based On')
    overtime = fields.Char(related='payslip_id.overtime', string='Overtime')
    ot_rate = fields.Float(related='payslip_id.ot_rate', string='OT Rate')