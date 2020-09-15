from odoo import models, fields, api, _
from odoo import exceptions 
from datetime import datetime


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
    
    def get_advance_salary_count(self):
        count = self.env['hr.employee.advance.salary'].search_count([('employee_id', '=', self.name)])
        self.advance_sal_req = count
    ad_check = fields.Boolean(string='Allow advance salary')    
    advance_sal_req = fields.Integer(string='Salary Request', compute='get_advance_salary_count')
    sal_limit = fields.Float(string='Advance Salary Request', store =True)
    sal_req_limit = fields.Integer(string='Advance Salary Limit', store=True,)
    
    
    

    
    
class EmployeeAdvanceSalary(models.Model):
    _name = 'hr.employee.advance.salary'
    _description = 'HR Employee Advance Salary'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'
    
    
    def payment_button(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'multi': False,
            'domain': [('communication','=', self.name)],
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
        }
    
    
    @api.model
    def action_send_email(self):
#         rec = super(ResPartnerInh, self).create(vals)
        
        #email when new partner created
        ctx = {}
#         email_list = ''
        email_list = self.env['res.users'].sudo().search(
            [('id', '=', self.uid.id)]) 
        
        if email_list:
            ctx['partner_manager_email'] = email_list
            ctx['email_from'] = self.env.user.email
            ctx['partner_name'] = self.env.user.name
#             ctx['customer_name'] = rec.name
            ctx['lang'] = self.env.user.lang
            template = self.env.ref('de_employee_advance_salary.email_template')
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            db = self.env.cr.dbname
            ctx['action_url'] = "{}/web?db={}#id={}&view_type=form&model=res.partner".format(base_url, db, self.id)
            
#             if self.env.cr.dbname == 'dont_use' or self.env.cr.dbname == 'oxvor_production' or self.env.cr.dbname == 'inhouse_testing':
            template.with_context(ctx).sudo().send_mail(rec.id, force_send=True, raise_exception=False)
        
        return 
    
#     def action_send_email(self):
        
#         #email when new partner created
#         ctx = {}
#         email_list = ''
#         email_list = [user.email for user in self.env['res.users'].sudo().search([])
        
# #         email_list = [user.email for user in self.env['res.users'].sudo().search([])         
# #         print("email list...",email_list)
# #         if email_list:
#         ctx['partner_manager_email'] = ','.join(
#                 [email for email in email_list if email])
#         ctx['email_from'] = self.env.user.email
#         ctx['partner_name'] = self.env.user.name
#         ctx['customer_name'] = rec.name
#         ctx['lang'] = self.env.user.lang
#         template = self.env.ref('de_employee_advance_salary.email_template')
#         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
# #            db = self.env.cr.dbname
# #             ctx['action_url'] = "{}/web?db={}#id={}&view_type=form&model=res.partner".format(base_url, db, self.id)
            
# #             if self.env.cr.dbname == 'dont_use' or self.env.cr.dbname == 'oxvor_production' or self.env.cr.dbname == 'inhouse_testing':
#         template.with_context(ctx).sudo().send_mail(rec.id, force_send=True, raise_exception=False)
        
#         return rec
    
    
    def action_send_email_t(self):
        
        self.ensure_one()
        self.request_date = datetime.today() 
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
        
        'force_email': True,   

        }
        self.write({
            'state': 'request',
        }) 

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
        self.write({
            'state': 'approval',
        }) 

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
        self.confirm_date = datetime.today()
        self.conf_manager_id = self._uid
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
        self.write({
            'state': 'hrconfirm',
         })  

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
        
              


    



    
    
    
    
    
    def action_case_send(self):
        template_id = self.env.ref('de_employee_disciplinary_case.email_template_edi_disciplinary_case').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.write({
            'state': 'response',
        })    
        
    def action_paid(self):
        if  not self.payment_method:
            raise exceptions.ValidationError('Please Define Payment Method and Paid amount.')
        vals = {
            'payment_type': 'outbound',
#             'partner_type': 'customer',
            'partner_id': self.employee_id.id,
            'amount': self.amount,
            'payment_date': self.confirm_date,
            'communication': self.name,
            'journal_id': self.payment_method.id,
            'payment_method_id': self.payment_method.id,

        }
        self.env['account.payment'].create(vals)
        self.write({
            'state': 'paid',
        })    
       
    def action_close_case(self):
        self.write({
            'state': 'close',
        })    
        

    name = fields.Char(string='Reference', readonly=True, copy=False,  index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', store=True, required=True)
    request_date = fields.Date(string='Request Date', store=True, readonly=True,)
    confirm_date = fields.Date(string='Confirm Date', store=True, readonly=True,)
    amount = fields.Float(string='Request Amount', store=True, required=True)
    manager_id = fields.Many2one('hr.employee',string='Department Manager', store=True, readonly=True,related='employee_id.parent_id')
    conf_manager_id = fields.Many2one('hr.employee',string='Confirm Manager', store=True, readonly=True,)
    emp_partner_id = fields.Many2one('hr.employee', string='Employee Partner', store=True, attrs={'required': ['|',('state','=', 'hrconfirm')]})
    payment_method = fields.Many2one('account.journal', string='Payment Method', store=True, attrs={'required': ['|',('state','=', 'hrconfirm')]})
    paid_amount = fields.Char(string='Paid Amount', store=True, attrs={'required': ['|',('state','=', 'hrconfirm')]})

    note = fields.Html(string="Reason" ,)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Request'),
        ('approval', 'Approval'),
        ('hrconfirm', 'HR Confirm'),        
        ('paid', 'Paid'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    department_id = fields.Many2one('hr.department', string='Department', readonly=True ,related='employee_id.department_id')
    
    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.employee.advance.salary') or _('New')
        user_obj = self.search([('employee_id','=', vals['employee_id'])])
        sum = 0
        for count in user_obj:
            sum = sum + 1
        if sum > self.employee_id.sal_req_limit:
            raise exceptions.ValidationError('You can create maximum'+ ' ' + str(self.employee_id.sal_limit) + ' ' + 'Advance Salary request Per Year.')
        else:
            pass        
#         seq = self.env['ir.sequence'].get('hr.employee.advance.salary') 
#         values['name'] = seq
        res = super(EmployeeAdvanceSalary,self).create(vals)
        return res
    
#     @api.multi
    def write(self, vals):
        user_obj = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name)])
        sum = 0
        for count in user_obj:
            sum = sum + 1
        if sum > self.employee_id.sal_req_limit:
            raise exceptions.ValidationError('You can create maximum'+ ' ' + str(self.employee_id.sal_req_limit) + ' ' + 'Advance Salary request Per Year.')
        else:
            pass        
#         seq = self.env['ir.sequence'].get('hr.employee.advance.salary') 
#         values['name'] = seq
#         res = super(EmployeeAdvanceSalary,self).create(vals) 
        res = super(EmployeeAdvanceSalary, self).write(vals)
        return res
    
    @api.onchange('employee_id')
    def onchange_employee(self):
        test_here = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name),('state','=', 'draft')])
        for rec in test_here:
            if rec.employee_id.name == self.employee_id.name:
                raise exceptions.ValidationError('You Have Already Create' +' '+ self.name + ' ' + 'Salary Request which is in draft.')
            else:
                pass
        if self.employee_id:    
            if self.employee_id.sal_limit == 0:
                raise exceptions.ValidationError('Plaese define' +' '+ str(self.employee_id.name) +' '+'Advance Salary Limit Amount.') 
        user_obj = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name)])
        sum = 0
        for count in user_obj:
            sum = sum + 1
        if sum > self.employee_id.sal_req_limit:
            raise exceptions.ValidationError('You can create maximum'+ ' ' + str(self.employee_id.sal_req_limit) + ' ' + 'Advance Salary request Per Year.')
        else:
            pass    
        
    
#     @api.onchange('employee_id')
#     def onchange_employee(self):
#         if self.employee_id.sal_limit == 0:
#             raise exceptions.ValidationError('Plaese define' + self.employee_id + 'Advance Salary Limit Amount')
        
    
    @api.onchange('amount')
    def onchange_amount(self):
        if self.employee_id.sal_limit < self.amount:
            raise exceptions.ValidationError('Advance Salary Amount Must be less than' + ' ' +str(self.employee_id.sal_limit))
        else:
            pass
            
#     @api.onchange('employee_id')
#     def onchange_employee(self):
#         user_obj = self.env['hr.employee.advance.salary'].search([('employee_id.name','=', self.employee_id.name)])
#         sum = 0
#         for count in user_obj:
#             sum = sum + 1
#         if sum > self.employee_id.sal_req_limit:
#             raise exceptions.ValidationError('You can create maximum'+ str(self.employee_id.sal_limit) + 'Advance Salary request Per Year.')
#         else:
#             pass
            
            
            