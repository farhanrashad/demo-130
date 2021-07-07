# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EmployeeInsurance(models.Model):
    _name = "hr.employee.insurance"


    @api.model
    def create(self,vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.insurance.sequence')
        
        if int(vals['amount']) <= 0:
            raise UserError(('Insurance amount must be greater than 0.'))
        
        result = super(EmployeeInsurance, self).create(vals)
        return result
    
#     @api.onchange('insurance_type')
#     def onchange_insurance_type(self):
#         if self.insurance_type:
#             self.description = str(self.insurance_type.name)+' is a contract between insurance holder and an insurer or assurer, where the insurer promises to pay a designated beneficiary a sum of money in exchange for a premium, upon the death of an insured person.'
    
    
#   declaring fields 
    name=fields.Char(string="Name",required=True,copy=False,readonly=True,index=True,default=lambda self: _('New'))
    employee_id=fields.Many2one("hr.employee",string="Employee")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    insurance_type=fields.Many2one("hr.employee.insurance.type",string="Insurance Type")
    amount = fields.Float(string="Amount")
    company_id=fields.Many2one('res.company','Company',readonly=True,default=lambda self:self.env.company.id)
    description=fields.Html(string="Description")
    state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('expired', 'Expired')],
                             string="State", default="draft",tracking=True)


    def action_activate(self):
        self.state = 'running'

    def action_expired(self):
        self.state = 'expired'
   
    
    
class EmployeeInsuranceType(models.Model):
    _name = "hr.employee.insurance.type"

#   declaring fields 
    name=fields.Char(string="Name",required=True)



class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _name = "hr.employee"
    
    insurance_ids = fields.One2many('hr.employee.insurance', 'employee_id', string="Insurance")
    