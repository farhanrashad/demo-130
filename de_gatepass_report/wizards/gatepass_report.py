# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar



class GatepassReport(models.TransientModel):
    _name = "gatepass.report.wizard"
    _description = "Employee Wizard"
    
    
    date_from=fields.Date(string="Date From",default=datetime.datetime.today())
    date_to=fields.Date(string="Date To",default=datetime.datetime.today()) 
    employee=fields.Many2many('hr.employee',string="Employee")
    
    def action_report_gen(self):
        data = {}
        data['form'] = self.read([  'employee', 'date_from', 'date_to'])[0]
        return self.env.ref('de_employee_attendance_report.employee_attendance_report').report_action(self, data=data, config=False)