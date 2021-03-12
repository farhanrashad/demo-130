# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar



class EmployeeAttandanceWizard(models.Model):
    _name = "employee.attendance.wizard"
    _description = "Employee Wizard"
    
    
#     declaring attandance wizard fields
    date_from=fields.Date(string="Date From",default=datetime.datetime.today())
    date_to=fields.Date(string="Date To",default=datetime.datetime.today()) 
    
#     all_emp=fields.Boolean(string="All Employees",default=True)
    employee=fields.Many2many('hr.employee',string="Employee")
    
    
    def action_report_gen(self):
        data = {}
        data['form'] = self.read([  'employee', 'date_from', 'date_to'])[0]
        return self.env.ref('openhcm_employee_attendance.attendance__report_pdf').report_action(self, data=data, config=False)
    
    
    
