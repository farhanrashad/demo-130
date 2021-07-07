# -*- coding: utf-8 -*-
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
#     @api.model
#     def create(self,vals):
#         res = super(HrPayslip,self).create(vals)
#         #For faster performance used query.
#         if res.date_from and res.date_to and res.contract_id:
#             self._cr.execute("select count(id) from hr_attendance where check_in::date>='%s' and check_out::date<='%s' and employee_id=%d"%(res.date_from,res.date_to,res.employee_id.id))
#             result = self._cr.fetchone()
#             if result and result[0]:
#                 self.env['hr.payslip.worked_days'].create({'name': '%s Attendances'%(res.employee_id.name),'number_of_days':result[0], 'code' : 'Attendance', 'payslip_id':res.id,'contract_id':res.contract_id.id})
#         return res
    @api.onchange('employee_id','date_from', 'date_to')
    def onchange_employee(self):       
        user_obj = self.env['hr.attendance'].search([('employee_id.name','=', self.employee_id.name),('check_in', '>=', self.date_from),('check_out', '<=', self.date_to)])
#         contract = self.contract_id
#         if contract.resource_calendar_id:
        if self.employee_id:
            hours = 0.0
            days = 0.0
            paid_amount = self._get_contract_wage()
            days = round(hours / 160, 5)

            
            for rec in user_obj:
                data = []
                hours = hours + rec.worked_hours
            data.append((0,0,{
                        'name': 'Attendance',
                        'work_entry_type_id': 1,
                        'number_of_days': round((hours/8),0),
                        'number_of_hours': hours,
                        'amount': paid_amount,
                        }))
            self.worked_days_line_ids = data
            
#     @api.onchange('employee_id')
#     def onchange_employee(self):
#         test = {
#                     'sequence': 1,
#                     'work_entry_type_id':1,
#                     'number_of_days': 2,
#                     'number_of_hours': 1,
#                     'payslip_id':5, 
#                     'amount': 4,
#                 }
#         newr = self.env['hr.payslip'].create(test)
#         attendance_line = {
#                     'payslip_id':newr, 
#                     'sequence': 1,
#                     'work_entry_type_id':1,
#                     'number_of_days': 2,
#                     'number_of_hours': 1,
#                     'amount': 4,
#                 }
#         ress = self.env['hr.payslip.worked_days'].create(attendance_line)
#         resss = super(HrPayslip, self)._get_worked_day_lines()

#         """
#         :returns: a list of dict containing the worked days values that should be applied for the given payslip
#         """
#         res = []
#         # fill only if the contract as a working schedule linked
#         self.ensure_one()
#         contract = self.contract_id
#         if contract.resource_calendar_id:
#             paid_amount = self._get_contract_wage()
#             unpaid_work_entry_types = self.struct_id.unpaid_work_entry_type_ids.ids

#             work_hours = contract._get_work_hours(self.date_from, self.date_to)
#             total_hours = sum(work_hours.values()) or 1
#             work_hours_ordered = sorted(work_hours.items(), key=lambda x: x[1])
#             biggest_work = work_hours_ordered[-1][0] if work_hours_ordered else 0
#             add_days_rounding = 0
#             for work_entry_type_id, hours in work_hours_ordered:
#                 work_entry_type = self.env['hr.work.entry.type'].browse(work_entry_type_id)
#                 is_paid = work_entry_type_id not in unpaid_work_entry_types
#                 calendar = contract.resource_calendar_id
#                 days = round(hours / calendar.hours_per_day, 5) if calendar.hours_per_day else 0
#                 if work_entry_type_id == biggest_work:
#                     days += add_days_rounding
#                 day_rounded = self._round_days(work_entry_type, days)
#                 add_days_rounding += (days - day_rounded)
#                 attendance_line = {
#                     'sequence': work_entry_type.sequence,
#                     'work_entry_type_id': work_entry_type_id,
#                     'number_of_days': day_rounded,
#                     'number_of_hours': hours,
#                     'amount': hours * paid_amount / total_hours if is_paid else 0,
#                 }
#                 ress = self.env['hr.payslip.worked_days'].create(attendance_line)
#                 res.append(attendance_line)
#         return resss


# 
#     @api.onchange('employee_id', 'date_from', 'date_to')
#     def onchange_employee_id(self):
# #         res = super(HrPayslip, self).onchange_employee_id()
#         lst = []
#         if self.date_from and self.date_to and self.contract_id:
#             self._cr.execute("select count(id) from hr_attendance where check_in::date>='%s' and check_out::date<='%s' and employee_id=%d" % (self.date_from, self.date_to, self.employee_id.id))
#             result = self._cr.fetchone()
#             if result and result[0]:
#                 lst.append({'name': '%s Attendances' % (self.employee_id.name),
#                             'number_of_days': result[0],
#                             'code' : 'Attendance',
#                             'contract_id': self.contract_id.id})
#             # leave
#             self._cr.execute("""select sum(number_of_days_temp)
#                                 from hr_holidays
#                                 where date_from::date >= '%s'
#                                 and date_to::date <= '%s'
#                                 and state = 'validate'
#                                 and type = 'remove'
#                                 and employee_id='%s'""" % (self.date_from, self.date_to, self.employee_id.id))
#             result = self._cr.fetchone()
#             print ("\n\n --payslip_attendance_ext--", result)
#             if result:
#                 lst.append({'name': '%s Leave' % (self.employee_id.name),
#                             'number_of_days': result[0] if result[0] else 0.00,
#                             'code' : 'Leave',
#                             'contract_id': self.contract_id.id})
#         #self.worked_days_line_ids = False
#         worked_days_lines = self.worked_days_line_ids.browse([])
#         for r in lst:
#             worked_days_lines += worked_days_lines.new(r)
#         self.worked_days_line_ids += worked_days_lines
#         return lst
