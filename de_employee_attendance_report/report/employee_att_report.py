# -*- coding: utf-8 -*-

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from odoo import api, fields, models, _

class AttendanceReport(models.AbstractModel):
    _name = 'report.de_employee_attendance_report.employee_template'
    
    def get_attendance(self, employee_id, date_from, date_to):
        vals = ''
        attendances = self.env['hr.attendance'].search([('employee_id', '=',employee_id.id ),('check_in_date', '>=', date_from),('check_in_date', '<=', date_to)])
        
        if attendances:
            vals = attendances
        else:
            pass
        return vals
        
    
    def _get_report_values(self, docids, data=None):
        all_emp = self.env['hr.employee'].search([])
        return {
            'doc_ids': self.ids,
            'doc_model': 'hr_attendance.hr.attendance',
            'get_attendance': self.get_attendance,
            'all_employees': all_emp,
            'date_from': data['form']['date_from'],
            'date_to': data['form']['date_to'],
        }