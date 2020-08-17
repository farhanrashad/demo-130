from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
from odoo.exceptions import Warning

   
class Job_MenuForm(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='hr.job.position.request'
    _description="Job Position Request"
    

 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('verify', 'Verified'),
        ('co_approve', 'COO Approved'),
        ('done', 'Done'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    
    def unlink(self):
        for leave in self:
            if leave.state in ('done','verify','co_approve'):
                raise UserError(_('You cannot delete an order form  which is not draft or cancelled. '))
     
            return super(Job_MenuForm, self).unlink()
    
   

        
    def draft(self):
        self.write({'state':'submit'}) 
        
    def submit(self):
        self.write({'state':'verify'}) 
        
    def verify(self):
        self.write({'state':'co_approve'})    
        
    def co_approve(self):
        self.env['hr.job'].create({'name': self.name,
                                            'department_id':self.department.id,
                                            'no_of_recruitment':self.no_of_person_request,
                                            'user_id':self.requested_by.id,
                                            })
        self.write({'state':'done'})    
   
   

    
    date=fields.Date("Date")
    no_of_person_request=fields.Integer('Numbers of Persons Requested',default="1")
    gender_preference=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('trans', 'Transgender'),
        ], string='Gender Preferences')
    budget=fields.Boolean('Budgeted')
    department=fields.Many2one('hr.department',"Department")
    team=fields.Many2one('hr.team','Team')
        
    requested_by=fields.Many2one('res.users','Requested By',  default=lambda self: self.env.user)
    reported_to=fields.Many2one('res.users','Reporting To')

    reason = fields.Text('Reason')
    job_position=fields.Many2one('hr.job','Job Position')
    age_preference=fields.Integer('Age Preference',default="0")
    get_id=fields.Char('Order', readonly=True, copy=False,)
    name= fields.Char('Name', required=True)
    qualification= fields.Html('Qualifications / Background / Skills Set')
    education= fields.Html('Education / Degree Required')
    software= fields.Html('Software Proficiency Requirements')
    communication= fields.Html('Communications')
    
    
    @api.model
    def create(self, vals):
        if 'get_id' not in vals or vals['get_id'] == False:
            sequence = self.env.ref('open_hcm_job_position_request.get_id')
            vals['get_id'] = sequence.next_by_id()
        return super(Job_MenuForm, self).create(vals)
    
    
class team_form(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='hr.team'
    _description="Team Form"


    name=fields.Char('Name',required=True)
    