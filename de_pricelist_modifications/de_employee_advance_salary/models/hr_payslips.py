from odoo import models, fields, api, _
from odoo import exceptions 
from datetime import datetime


class HrPayslipsInherit(models.Model):
    _inherit = 'hr.payslip'
    
    def compute_sheet(self):
        res = super(HrPayslipsInherit, self).compute_sheet()
        other_inputs = self.env['hr.payslip.input'].search([('code','=', 'ADV')])
        paid_amount = self.env['hr.employee.advance.salary'].search([('employee_id','=', self.employee_id.id),('state','=', 'paid')])
        for sal_amount in paid_amount: 
            for rec in other_inputs:
                data = []
                data.append((0,0,{
                            'input_type_id': rec.id,
                            'amount': sal_amount.amount,
                            }))
            self.input_line_ids = data
        return res
    
    

    
    

            
            