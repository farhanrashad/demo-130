# -*- coding: utf-8 -*-

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from odoo import api, fields, models, _

class AttendanceReport(models.AbstractModel):
    _name = 'report.de_employee_attendance_report.employee_template'
    
    def get_attendance(self, employee_id):
        attendences = self.env['hr.attendance'].search([('check_in_date', '>=', rec.start_date),('check_in_date', '<=', rec.end_date),('employee_id', '=',employee_id.id )])
        
        if attendances:
            vals = attendances
        else:
            pass
        return vals
        
    
    def _get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        rec = self.env[self.model].browse(self.env.context.get('active_id'))
        all_emp = self.env['hr.employee'].search([])
        

        return {
            'doc_ids': self.ids,
            'doc_model': 'hr_attendance.hr.attendance',
#             'docs': docs,
            'get_attendance': self.get_attendance,
            'rec': rec,
            'all_employees': all_emp,
        }