# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime
        
        
        
class HrEmployeeInh(models.Model):
    _inherit = 'hr.employee'
    
    relation_with = fields.Char('S/O-W/O-D/O')
    is_disable = fields.Boolean('Disable?')
    age = fields.Char('Age', compute='onchange_birthday')
    religion = fields.Selection([('Islam','Islam'), ('Christian','Christian'), ('Hindu','Hindu')], 
                                string='Religion')
    referee_person = fields.Char('Referee Person')
    equipment_acquired = fields.Char('Equipment Acquired')
    
    
    contract_start_date = fields.Date(compute='compute_salary')
    salary = fields.Char('Salary', compute='compute_salary')
    
    sequence_no = fields.Char('Sequence No.', required=True, readonly=True, default=lambda self: _('New'))
    
    
    @api.model
    def create(self,vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hr.employee.sequence')
        
        result = super(HrEmployeeInh, self).create(vals)
        return result
    
    
    
    def onchange_birthday(self):
        dob = self.birthday
        if dob:
            today = date.today()
            self.age = str(today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)))+" Years"
        else:
            self.age = '-'
    
    
    def compute_salary(self):
        for rec in self:
            if rec.contract_id and rec.contract_id.state == 'open':
                rec.salary = rec.contract_id.wage
                rec.contract_start_date = rec.contract_id.date_start
                
            else:
                rec.salary = '-'
                rec.contract_start_date = None
    
    
    
    
    