# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import date, datetime
gloabal_list = []


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    sale_commission_account = fields.Many2one(comodel_name='account.account', string='Commission Account')
    commission_pay_by = fields.Selection([
        ('sal', 'Salary'),
        ('inv', 'Invoice')],
        string='Commission Pay By')


class CommissionForm(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name = 'commission.rule'
    _description = 'Commission Rule'

    commission_order_line = fields.One2many(comodel_name='commission.orderline', inverse_name='id_order')
    logged_user = fields.Many2one(comodel_name='res.users', string='Created By',
                                  default=lambda self: self.env.user)
    notes = fields.Text(string='Terms and Conditions')
    name = fields.Char(string='Name', required=True)
    
    

    
    
        
    
class CommissionProcessLineForm(models.Model):
    _name = 'commission.orderline'
    _description = 'Commission Process Form'

    id_order = fields.Many2one(comodel_name='commission.rule')
    date_to = fields.Date(string='Date To')
    date_from = fields.Date(string='Date From')
    priority = fields.Integer(string='Priority', default='1')
    apply_on = fields.Selection([
        ('pos', 'POS Order'),
        ('sale', 'Sale Order')],
        string='Type', default='pos')


class PosConfigExt(models.Model):
    _inherit = 'pos.config'
    
    commission_rule_group = fields.Many2one(comodel_name='commission.rule', string='Commission Rule Group')
    
    
class PosOrderExt(models.Model):
    _inherit = 'pos.order'
    
    pos_sale_line = fields.One2many(comodel_name='pos.sale.commission', inverse_name='psl_order')

    @api.model
    def create(self, values):
        picking = super(PosOrderExt, self).create(values)
        if values:
            dt = []
            rules = self.env['create.rule.form'].search([])
            for rule in rules:
                if str(rule.start_date) <= values['date_order'].split()[0] and str(rule.end_date) >= values['date_order'].split()[0]:
                    rule_record = self.env['create.rule.form'].search([('id', '=', rule.id)])
                    if values['amount_total'] >= rule_record.minimum_order:
                        for line in rule_record.rule_line:
                            if line.employee_id.id == values['employee_id']:
                                self.env['commission.form'].create({
                                        'source_document': str(values['lines'][0][2]['name']),
                                        'employee_id': line.employee_id.id,
                                        'order_date': values['date_order'].split()[0],
                                        'sales_amount': values['amount_total'],
                                        'commission_amount': values['amount_total']*(line.commission_price/100),
                                        'session_id': values['session_id']
                                    })
        return picking
            
    @api.onchange('state')
    def onchange_func_state(self):
        for order in self:
            if order.state == 'paid':
                rule_form = self.env['create.rule.form'].search([])
                for rule in rule_form:
                    if rule.start_date<=self.date_order.date() and rule.end_date>=self.date_order.date():
                        z = self.env['create.rule.form'].search([('id', '=', rule.id)])
                        if self.amount_total >= z.minimum_order:
                            for zz in z.rule_line:
                                self.env['commission.form'].create({
                                        'source_document': self.name,
                                        'employee_id': zz.employee_id.id,
                                        'order_date': self.date_order.date(),
                                        'sales_amount': self.amount_total,
                                        'commission_amount': ((zz.commission_price/100)*self.amount_total),
                                        'pos_order': self.id,
                                        'payment_id': self.payment_ids.id,
                                    })
    

class PosOrderLineExt(models.Model):
    _name = 'pos.sale.commission'
    
    psl_order = fields.Many2one(comodel_name='pos.order', string='Order')
    user_id = fields.Many2one(comodel_name='res.users', string='User')
    job_position = fields.Many2one(comodel_name='hr.job', string='Job Position')
    commission_amount = fields.Float(string='Commission Amount')


class RuleCreation(models.Model):
    _name = 'create.rule.form'
    _rec_name = 'apply_on'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    apply_on = fields.Selection([
        ('pos', 'Pos Order')],
        string='Apply On',
        default='pos')
    priority = fields.Integer(string='Priority', default='1')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    minimum_order = fields.Float(string='Minimum Order Amount')
    rule_line = fields.One2many(comodel_name='beneficial.form', inverse_name='rule_order')

    @api.constrains('minimum_order')
    def ks_check_commission_amount(self):
        if self.minimum_order <= 0:
            raise ValidationError('Minimum Order amount should be greater than 0.')
            
    @api.model
    def create(self, values):
        rules = super(RuleCreation, self).create(values)
        rules = self.env['create.rule.form'].search([])
        for rule in rules:
            if str(rule.start_date) <= values['start_date'] and str(rule.end_date) >= values['end_date']:
                raise UserError(_('You cannot create Rule between date' + values['start_date'] + ' ' + 'to' + ' '+ values['end_date']))
        return rules        
            

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    employee_set = fields.Boolean(string='Employee Selected')

class BeneficialForm(models.Model):
    _name = 'beneficial.form'

    @api.model
    def _employee_domain(self):
        # for rec in self:
        list = []
        line_item = self.env['beneficial.form'].search([('rule_order', '=', self._origin.id)])
        for line in line_item:
            gloabal_list.append(line.employee_id.id)
        return gloabal_list

#     @api.onchange('employee_id')
#     def onchange_test_domain_fiedl(self):
#         # here use your model to fetch the records
#         obj = self.search([])
#         available_ids = []
#         for i in obj:
#             # appends the man2one fields idsss
#             available_ids.append(i.employee_id.id)
#         return {'domain': {'employee_id': [('id', 'not in', available_ids)]}}
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True, domain="[('employee_set', '=', False)]")
    job_title = fields.Char(related='employee_id.department_id.name')
    
    @api.onchange('employee_id')
    def onchange_employee(self):
        if self.employee_id:
            employees  = self.env['hr.employee'].search([('name','=', self.employee_id.name)])
            for employee in employees:
                employee.update ({
                    'employee_set': True,
                })
    
    # users = fields.Many2one('res.users', string='User')
    user_id = fields.Many2one(comodel_name='res.users', string='User')
    compute_price = fields.Selection([
        ('percentage', 'Percentage')],
        string='Compute Price')
    commission_price = fields.Float(string='Commission(%)')
    rule_order = fields.Many2one(comodel_name='create.rule.form')


class EmployeeCommissionForm(models.Model):
    _name = 'commission.form'
    _rec_name = 'source_document'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    source_document = fields.Char(string='Source Document', readonly=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)
    invoice = fields.Many2one(comodel_name='account.move', string='Invoice', readonly=True,
                              domain=[('type', '=', ('in_invoice'))])
    order_date = fields.Date(string='Order Date', readonly=True)
    sales_amount = fields.Float(string='Sales Amount', readonly=True)
    commission_amount = fields.Float(string='Commission Amount', readonly=True)
    pay_by = fields.Selection([
        ('sal', 'Salary'),
        ('inv', 'Invoice')],
        string='Pay By')
    pos_order = fields.Char(string='Pos Order')
    payment_id = fields.Char(string='Payment Id')
    session_id = fields.Many2one(comodel_name='pos.session', string='Session')
    config_id = fields.Many2one(comodel_name='pos.config', string='Outlet', related='session_id.config_id')


class SalesTarget(models.Model):
    _name = 'sales.target.form'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    def set_draft(self):
        self.write({'state': 'confirm'})
    
    sales_person = fields.Many2one(comodel_name='res.users', string='Sales Person')
    target_period = fields.Selection([
        ('mt', 'Monthly'),
        ('yl', 'yearly'),
        ('dy', 'Day')],
        string='Target Period', default="mt")
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    sales_target_line = fields.One2many(comodel_name='sale.target.line', inverse_name='sale_target_order')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'confirmed')],
        string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')


class SalesTargetLine(models.Model):
    _name = 'sale.target.line'

    start_target = fields.Date(string='Start of Target')
    end_target = fields.Date(string='End of Target')
    target_amount = fields.Float(string='Target Amount')
    sale_amount = fields.Float(string='Sales Amount')
    commission_amount = fields.Float(string='Commission Amount')
    sale_target_order = fields.Many2one(comodel_name='sales.target.form', string='Target')


class PrintCommissionSummary(models.Model):
    _name = 'commission.summary'
    _description = 'Create commission summary'
    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    all_employee = fields.Boolean(string='All Employee')
    employee_id = fields.Many2many(comodel_name='hr.employee', string='Employee')
    user = fields.Many2many(comodel_name='res.users', string='User(s)')
    
    @api.onchange('all_user')
    def user_auto(self):
        if self.all_user==True:
            user_list = self.env['res.users'].search([])
            self.user = user_list

    def create_invoice(self):
        for order in self:
            invoice_line_ids = []
            if (order.start_date and order.end_date):
                invoice_line = []
                list = []
                account = self.env['account.account'].search([('name', '=', 'POSCommission')])
                commission_data = self.env['commission.form'].search([])
                for data in commission_data:
                    invoice_lines = {
                        'name': data.source_document,
                        'account_id': account.id,
                        'quantity': 1.0,
                        'price_unit': data.commission_amount,
                    }
                    for employee in order.employee_id:
                        if order.start_date <= data.order_date and order.end_date >= data.order_date:
                            if employee.id == data.employee_id.id:
                                list.append(data)
                                inv_obj = {
                                    'partner_id': data.employee_id.user_id.partner_id.id,
                                    'invoice_date': fields.Date.today(),
                                    'type': 'in_invoice',
                                    'name': 'Commission Invoice',
                                    'state': 'draft',
                                    'invoice_line_ids': [(0, 0, invoice_lines)],
                                }
                                record = self.env['account.move'].create(inv_obj)
