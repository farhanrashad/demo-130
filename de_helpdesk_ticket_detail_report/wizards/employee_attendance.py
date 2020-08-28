# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class EmployeeAttandanceWizard(models.Model):
    _name = "employee.attendance.wizard"
    _description = "Employee Wizard"
    
    
#     declaring attandance wizard fields
    current_date=fields.Date(string="Date",default=datetime.today())
    print_by = fields.Selection([('daily', 'Daily'),
                                   ('weekly', 'Weekly'),
                                 ('monthly', 'Monthly')],default="daily")
    all_emp=fields.Boolean(string="All Employees",default=True)
    employee=fields.Many2many('hr.employee',string="Employee")





    @api.onchange('all_emp')
    def _get_sel_emp(self):
        if self.all_emp==True:
            print("it was true--------------")
            return
        else:
            print("it was false------------")
            self.all_emp=False

    def action_report_gen(self):
        print("called----------------------------")
        print("many2many emp are ",self.employee,type(self.employee))
        emp_name={}
        count=0
        for temp in self.employee:
                emp_name[self.employee[count].id]=self.employee[count].name
                count=count+1
        print("selected emp  ara------------",emp_name)
        if not self.current_date:
            raise UserError(_("Please Select Date"))
            return
        datas = {
            'current_date': self.current_date,
            'print_by': self.print_by,
            'all_emp': self.all_emp,
            'emp_sel':emp_name
        }
        return self.env.ref('openhcm_employee_attendance.emp_att_xlsx').report_action(self,data=datas)