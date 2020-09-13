from odoo import models, fields, api, _
from odoo import exceptions 

class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    
    def salary_request(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'hr.employee.advance.salary',
            'view_mode': 'tree,form',
        }

    sal_limit = fields.Float(string='Advance Salary Request', store =True)
    sal_req_limit = fields.Integer(string='Advance Salary Limit', store=True, required=True)
    

    
    
class EmployeeAdvanceSalary(models.Model):
    _name = 'hr.employee.advance.salary'
    _description = 'HR Employee Advance Salary'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    
    def action_send_email(self):
       self.ensure_one()
       ir_model_data = self.env['ir.model.data']
       try:
           template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template')[1]
       except ValueError:
        template_id = False
       try:
           compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
       except ValueError:
           compose_form_id = False
       ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
       'default_template_id': template_id,

       'default_composition_mode': 'comment',

       }

       return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

       }
       self.write({
            'state': 'request',
        }) 
        
    
    def action_send_email_approve(self):
       self.ensure_one()
       ir_model_data = self.env['ir.model.data']
       try:
           template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_approve')[1]
       except ValueError:
        template_id = False
       try:
           compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
       except ValueError:
           compose_form_id = False
       ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
       'default_template_id': template_id,

       'default_composition_mode': 'comment',

       }

       return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

       }
       self.write({
            'state': 'approval',
        }) 
        
    
    
    def action_send_email_reject(self):
       self.ensure_one()
       ir_model_data = self.env['ir.model.data']
       try:
           template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_reject')[1]
       except ValueError:
        template_id = False
       try:
           compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
       except ValueError:
           compose_form_id = False
       ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
       'default_template_id': template_id,

       'default_composition_mode': 'comment',

       }

       return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

       }
    
    def action_send_email_confirm(self):
       self.ensure_one()
       ir_model_data = self.env['ir.model.data']
       try:
           template_id = \
               ir_model_data.get_object_reference('test_email', 'email_template_confirm')[1]
       except ValueError:
        template_id = False
       try:
           compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
       except ValueError:
           compose_form_id = False
       ctx = {

           'default_model': 'hr.employee.advance.salary',

           'default_res_id': self.ids[0],

           'default_use_template': bool(template_id), 
       'default_template_id': template_id,

       'default_composition_mode': 'comment',

       }

       return {

           'name': _('Compose Email'),

           'type': 'ir.actions.act_window',

           'view_mode': 'form',

           'res_model': 'mail.compose.message',

           'views': [(compose_form_id, 'form')],

           'view_id': compose_form_id,

           'target': 'new',

           'context': ctx,

       }
       self.write({
            'state': 'hrconfirm',
        })  
              


    



    
    
    
    
    
    def action_case_send(self):
        template_id = self.env.ref('de_employee_disciplinary_case.email_template_edi_disciplinary_case').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'state': 'response',
        })    
        
    def action_paid(self):
        vals = {
            'payment_type': 'outbound',
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'amount': self.amount,
            'payment_date': self.confirm_date,
            'communication': self.name,
            'journal_id': self.payment_method.id,
        }
        self.env['account.payment'].create(vals)
        self.write({
            'state': 'paid',
        })    
       
    def action_close_case(self):
        self.write({
            'state': 'close',
        })    
        

    name = fields.Char(string='Reference',  copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True, required=True)
    request_date = fields.Date(string='Request Date', store=True, required=True)
    confirm_date = fields.Date(string='Confirm Date', store=True)
    amount = fields.Float(string='Request Amount', store=True, required=True)
    manager_id = fields.Many2one('hr.employee',string='Department Manager', store=True, required=True)
    conf_manager_id = fields.Many2one('hr.employee',string='Confirm Manager', store=True)
    emp_partner_id = fields.Many2one('res.users', string='Employee Partner', store=True)
    payment_method = fields.Many2one('account.jounal', string='Payment Method', store=True)
    paid_amount = fields.Char(string='Paid Amount', store=True)

    note = fields.Char(string="Reason" , required = True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Request'),
        ('approval', 'Approval'),
        ('hrconfirm', 'HR Confirm'),        
        ('paid', 'Paid'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    department_id = fields.Many2one('hr.department', string='Department')
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('hr.employee.advance.salary') 
        values['name'] = seq
        res = super(EmployeeAdvanceSalary,self).create(values)
        return res
    
    @api.onchange('employee_id')
    def onchange_employee(self):
        test_here = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name),('state','=', 'draft')])
        for rec in test_here:
            if rec.employee_id.name == self.employee_id.name:
                raise exceptions.ValidationError('You Have Already Create' + self.name + 'Salary Request which is in draft.')
            else:
                pass
        
    
    @api.onchange('employee_id')
    def onchange_employee(self):
#         user_obj = self.env['hr.attendance'].search([('employee_id.name','=', self.employee_id.name)])
        if self.employee_id.sal_limit == 0:
            raise exceptions.ValidationError('Plaese define' + self.employee_id + 'Advance Salary Limit Amount')
        elif self.employee_id.sal_limit < self.amount:
            raise exceptions.ValidationError('Advance Salary Amount Must be less than' + self.employee_id.sal_limit)
        else:
            pass
            
    @api.onchange('employee_id')
    def onchange_employee(self):
        user_obj = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name)])
        sum = 0
        for count in user_obj:
            sum = sum + 1
        if sum > self.employee_id.sal_req_limit:
            raise exceptions.ValidationError('You can create maximum'+ self.employee_id.sal_limit + 'Advance Salary request Per Year.')
        else:
            pass
            
            
            