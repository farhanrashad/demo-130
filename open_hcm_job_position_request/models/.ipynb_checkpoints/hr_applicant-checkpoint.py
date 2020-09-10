from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning

   

    
class HrApplicant(models.Model):
    _inherit='hr.applicant'


#     pref_name=fields.Char('Name',required=True)
#     pref_value=fields.Char('Value',required=True)
    skill_id=fields.One2many('hr.skill',  'applicant_id', string='Skills',)
    
class HrSkill(models.Model):
    _name='hr.skill'
    _description = 'This is skill set'


    pref_name=fields.Char('Name',required=True)
    pref_value=fields.Char('Value',required=True)
    applicant_id=fields.Many2one('hr.applicant', string='')    


        
