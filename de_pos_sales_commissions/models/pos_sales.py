# -*- coding: utf-8 -*-

from odoo import api, fields, models,_

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sale_commission_account = fields.Many2one('account.account',string="Commission Account")
    
    commission_pay_by = fields.Selection([('sal','Salary'),('inv','Invoice')],string="Commission Pay By")

class commission_Form(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='commission.rule'
    _description="Commission Rule Group"
    

    commission_order_line=fields.One2many("commission.orderline","id_order")
        
    logged_user=fields.Many2one('res.users','Created By',  default=lambda self: self.env.user)
    
    notes = fields.Text('Terms and Conditions')

    
    name= fields.Char('Name', copy=False)
        
    
class commission_processLine_Form(models.Model):
  
    _name='commission.orderline'
    _description="Rules"
    
     
    id_order=fields.Many2one("commission.rule") 
    date_to=fields.Date("Date To")  
    date_from=fields.Date("Date From")  

    priority=fields.Integer("Priority",default="1")
    apply_on=fields.Selection([ ('pos', 'POS Order'),('sale', 'Sale Order'),],'Type', default='pos')
   
class config(models.Model):
    _inherit='pos.config'
    
    commission_rule_group = fields.Many2one('commission.rule',string="Commission Rule Group")
    
    
class pos_order(models.Model):
    _inherit='pos.order'
    
    pos_sale_line=fields.One2many("pos.sale.commission","psl_order")
    
    
    @api.model
    def create(self, values): 
        if values:
            dt=[] 
            k=self.env['create.rule.form'].search([]) 
            for kk in k:
                if str(kk.start_date)<=values['date_order'].split()[0] and values['date_order'].split()[0]>=str(kk.end_date):
                        z=self.env['create.rule.form'].search([('id','=',kk.id)])
                        if values['amount_total'] >=z.minimum_order:
                            for zz in z.rule_line:
                                if zz.compute_price=='percentage':
                                    self.env['commission.form'].create({'source_document': str(values['lines'][0][2]['name']),
                                                                    'User':zz.users.id,
                                                                    'order_date':values['date_order'].split()[0],
                                                                    'sales_amount':values['amount_total'],
                                                                    'commission_amount':values['amount_total']*zz.commission_price,
                                                                    })
                else:
                    k=0
                
        return super(pos_order, self).create(values)
            
    @api.onchange('state')
    def onchange_func_state(self):
        for order in self:
            if order.state == 'paid':
                k=self.env['create.rule.form'].search([]) 
                for kk in k:
                    if kk.start_date<=self.date_order.date() and self.date_order.date()>=kk.end_date:
                            z=self.env['create.rule.form'].search([('id','=',kk.id)])
                            if self.amount_total >=z.minimum_order:
                                for zz in z.rule_line:
                                    if zz.compute_price=='percentage':
                                        line =self.env['commission.form'].create({'source_document': self.name,
                                                                    'User':zz.users_id.id,
                                                                    'order_date':self.date_order.date(),
                                                                    'sales_amount':self.amount_total,
                                                                    'commission_amount':0.0,
                                                                    'pos_order':self.id,
                                                                   'payment_id':self.payment_ids.id,
                                                                    })
    

class pos_order_line(models.Model):
    _name='pos.sale.commission'   
    
    psl_order=fields.Many2one("pos.order") 
    User=fields.Many2one('res.users',string="User")
    job_position=fields.Many2one('hr.job',string="Job Position")
    commission_amount=fields.Float("Commission Amount")
    
class create_rule(models.Model):
    _name='create.rule.form' 
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    
    apply_on=fields.Selection([('one','Product Variant'),('two','Product Catgory'),('three','Pos Order')],'Apply On',default="three")
    priority=fields.Integer("Priority",default="1")
    start_date=fields.Date("Start Date")
    end_date=fields.Date("End Date")
    minimum_order=fields.Float("Minimum Order")
    rule_line=fields.One2many("beneficial.form","rule_order")
    
class beneficial(models.Model):
    _name='beneficial.form'
    
    
    job_title=fields.Many2one('hr.job',string="Job Title")
    users=fields.Many2one('res.users',string="User(s)")
    compute_price=fields.Selection([('f_x','Fix Price'),('percentage','Percentage')],'Compute Price')
    commission_price=fields.Float("Commission")
    rule_order=fields.Many2one("create.rule.form") 

class commission(models.Model):
    _name='commission.form' 
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    source_document=fields.Char("Source Document")
    User=fields.Many2one('res.users',string="User")
    invoice=fields.Many2one('account.move',"Invoice" ,domain=[('type','=',('in_invoice'))])
    order_date=fields.Date("Order Date")
    sales_amount=fields.Float("Sales Amount")
    commission_amount=fields.Float("Commission Amount")
    pay_by=fields.Selection([('sal','Salary'),('inv','Invoice')],'Pay By')
    pos_order=fields.Char("Pos Order")
    payment_id=fields.Char("Payment Id")

class sales_target(models.Model):
    _name='sales.target.form' 
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin'] 
    
    sales_person=fields.Many2one('res.users',string="Sales Person")
    target_period=fields.Selection([('mt','Monthly'),('yl','yearly'),('dy','Day')],'Target Period',default="mt")
    start_date=fields.Date("Start Date")
    end_date=fields.Date("End Date")
    
    sales_target_line=fields.One2many("sale.target.line","sale_target_order")
    
    state=fields.Selection([('draft','Draft'),('confirm','confirmed')],'Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    
    def draft(self):
        self.write({'state':'confirm'}) 
        
        

class sales_target_line(models.Model):
    _name='sale.target.line'
    
    
    start_target=fields.Date("Start of Target")
    end_target=fields.Date("End of Target")
    target_amount=fields.Float("Target Amount")
    sale_amount=fields.Float("Sales Amount")
    commission_amount=fields.Float("Commission Amount")
    sale_target_order=fields.Many2one("sales.target.form") 

class print_commission_summary(models.Model):
    _name = 'commission.summary'
    _description = 'Create commission summary'
    
    start_date=fields.Date("Start Date")
    end_date=fields.Date("End Date") 
    all_user=fields.Boolean('All User')
    user=fields.Many2many('res.users',string="User(s)")
    
    @api.onchange('all_user')
    def user_auto(self):
        if self.all_user==True:
            j=self.env['res.users'].search([])
            self.user = j  
        
        
    def create_invoice(self):
        for order in self:
            if (order.start_date and order.end_date and order.user):
                invoice_line = []
                us=[]
                jj=self.env['commission.form'].search([])
                for j in jj:
                    for od in order.user:
                        if order.start_date<=j.order_date and order.end_date>=j.order_date:
                            if od.id==j.User.id:
                                us.append(j)
                                for ss in j:
                                    self.env['commission.form'].search([('id','=',ss.id)])
                                    invoice_vals = {
                                        'type': 'in_invoice',
                                        'name':'/',
                                        'partner_id': ss.User.partner_id.id,
                                        'state': 'draft',
                                        'invoice_date':ss.order_date,
                                        'invoice_payment_term_id': '',
                                        'invoice_line_ids': [0, 0, {
                                            'name': ss.source_document,
                                            'account_id': '',
                                            'analytic_account_id': '',
                                           'quantity': 1.0,
                                           'price_unit':ss.commission_amount,
                                        }]
                                    }
                                    invoice = self.env['account.move'].sudo().create(invoice_vals)
     
     
        
     
     
 
     
     
     
     
     
     