from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import date, datetime


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_commission_account = fields.Many2one('account.account', string="Commission Account")
    commission_pay_by = fields.Selection([('sal', 'Salary'), ('inv', 'Invoice')], string="Commission Pay By")


class commission_Form(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name = 'commission.rule'
    _description = "Commission Rule Group"

    commission_order_line = fields.One2many("commission.orderline", "id_order")
    logged_user = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    notes = fields.Text('Terms and Conditions')
    name = fields.Char('Name', copy=False)


class commission_processLine_Form(models.Model):
    _name = 'commission.orderline'
    _description = "Rules"

    id_order = fields.Many2one("commission.rule")
    date_to = fields.Date("Date To")
    date_from = fields.Date("Date From")
    priority = fields.Integer("Priority", default="1")
    apply_on = fields.Selection([('pos', 'POS Order'), ('sale', 'Sale Order'), ], 'Type', default='pos')


class config(models.Model):
    _inherit = 'pos.config'

    commission_rule_group = fields.Many2one('commission.rule', string="Commission Rule Group")


class pos_order(models.Model):
    _inherit = 'pos.order'

    pos_sale_line = fields.One2many("pos.sale.commission", "psl_order")

    @api.model
    def create(self, values):
        if values:
            dt = []
            rules = self.env['create.rule.form'].search([])
            for rule in rules:
                if str(rule.start_date) <= values['date_order'].split()[0] and str(rule.end_date) >= \
                        values['date_order'].split()[0]:

                    rule_records = self.env['create.rule.form'].search([('id', '=', rule.id), ('state', '=', 'lock')])
                    if values['amount_total'] >= rule_records.minimum_order:
                        for line in rule_records.rule_line:
                            if line.job_title.id == values['employee_id']:
                                self.env['commission.form'].create({
                                    'source_document': str(values['lines'][0][2]['name']),
                                    'active_employee': values['employee_id'],
                                    'order_date': values['date_order'].split()[0],
                                    'sales_amount': values['amount_total'],
                                    'commission_amount': values['amount_total'] * (line.commission_price / 100),
                                })
                else:
                    k = 0
        return super(pos_order, self).create(values)

    @api.onchange('state')
    def onchange_func_state(self):
        for order in self:
            if order.state == 'paid':
                k = self.env['create.rule.form'].search([])
                for kk in k:
                    if kk.start_date <= self.date_order.date() and kk.end_date >= self.date_order.date():
                        z = self.env['create.rule.form'].search([('id', '=', kk.id)])
                        if self.amount_total >= z.minimum_order:
                            for zz in z.rule_line:
                                self.env['commission.form'].create({
                                    'source_document': self.name,
                                    'User': zz.users_id.id,
                                    'order_date': self.date_order.date(),
                                    'sales_amount': self.amount_total,
                                    'commission_amount': ((zz.commission_price / 100) * self.amount_total),
                                    'pos_order': self.id,
                                    'payment_id': self.payment_ids.id,
                                })


class pos_order_line(models.Model):
    _name = 'pos.sale.commission'

    psl_order = fields.Many2one("pos.order")
    User = fields.Many2one('res.users', string="User")
    job_position = fields.Many2one('hr.job', string="Job Position")
    commission_amount = fields.Float("Commission Amount")


class create_rule(models.Model):
    _name = 'create.rule.form'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'name'

    name = fields.Char(required=True)
    apply_on = fields.Selection([('pos', 'Pos Order')], 'Apply On', default="pos")
    priority = fields.Integer("Priority", default="1")
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    minimum_order = fields.Float("Minimum Order")
    rule_line = fields.One2many("beneficial.form", "rule_order")
    all_employees = fields.Boolean(string="Select All Employees", default=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('lock', 'Lock'),
    ], store=True, default='draft')

    @api.constrains('minimum_order')
    def check_commission_amount(self):
        if self.minimum_order <= 0:
            raise ValidationError('Minimum Order amount should be greater than 0.')

    @api.constrains('end_date', 'start_date')
    def date_constrains(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))

    @api.onchange('all_employees')
    def onchange_all_employees(self):
        employees = self.env['hr.employee'].search([])
        data = []
        if not self.all_employees == True:
            for line in self.rule_line:
                line.unlink()

        if self.all_employees:
            for line in self.rule_line:
                line.unlink()
            for employee in employees:
                data.append((0, 0, {
                    'job_title': employee.id,
                }))
            self.rule_line = data

    def action_lock(self):
        self.state = 'lock'
        self.refresh_employee_list()

    def refresh_employee_list(self):
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            employee.update({
                'employee_set': False,
            })

    def action_reset(self):
        self.state = 'draft'
        emp_list = []
        if self.rule_line:
            for line in self.rule_line:
                emp_list.append(line.job_title.id)

        employees = self.env['hr.employee'].search([('id', 'in', emp_list)])
        for employee in employees:
            employee.update({
                'employee_set': True,
            })

    @api.model
    def create(self, values):
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            employee.update({
                'employee_set': False,
            })
        rules = super(create_rule, self).create(values)
        return rules

    def write(self, values):
        emp_list = []
        if self.rule_line:
            for line in self.rule_line:
                emp_list.append(line.job_title.id)

        employees = self.env['hr.employee'].search([('id', 'in', emp_list)])

        for employee in employees:
            employee.update({
                'employee_set': True,
            })
        rules = super(create_rule, self).write(values)
        return rules


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    employee_set = fields.Boolean()


class beneficial(models.Model):
    _name = 'beneficial.form'

    job_title = fields.Many2one('hr.employee', string="Employee", domain=[('employee_set', '=', False)], required=True)
    users = fields.Many2one(related='job_title.job_id')
    compute_price = fields.Selection([('percentage', 'Percentage')], default='percentage', readonly=True)
    commission_price = fields.Float("Commission(%)")
    rule_order = fields.Many2one("create.rule.form")

    @api.onchange('job_title')
    def onchange_production_order(self):
        if self.job_title:
            employee_names = self.env['hr.employee'].search([('name', '=', self.job_title.name)])
            for employee_name in employee_names:
                employee_name.update({
                    'employee_set': True,
                })


#     @api.onchange('users')
#     def onchange_user(self):
#         for s in self:
#             l=self.env['hr.employee'].search([('name','=',s.users.name)])
#             if l:
#                 s.job_title=l.job_id.id
#             else:
#                 s.job_title=''


class commission(models.Model):
    _name = 'commission.form'
    _order = 'order_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    source_document = fields.Char("Source Document", readonly=True)
    User = fields.Many2one('res.users', string="User", readonly=True)
    active_employee = fields.Many2one('hr.employee', string='Cashier')
    invoice = fields.Many2one('account.move', "Invoice", domain=[('type', '=', ('in_invoice'))])
    order_date = fields.Date("Order Date")
    sales_amount = fields.Float("Sales Amount")
    commission_amount = fields.Float("Commission Amount")
    pay_by = fields.Selection([('sal', 'Salary'), ('inv', 'Invoice')], 'Pay By')
    pos_order = fields.Char("Pos Order")
    payment_id = fields.Char("Payment Id")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('billed', 'Billed'),
    ], store=True, default='draft')

    def action_cancelled(self):
        self.state = 'cancelled'

    def unlink(self):
        if not self.state == 'draft':
            raise UserError(('Deletion is only allowed for draft documents!'))

    def action_done(self):
        self.state = 'done'

    def action_billed(self):
        self.state = 'billed'


class print_commission_summary(models.Model):
    _name = 'commission.summary'
    _description = 'Create commission summary'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    all_user = fields.Boolean('All Employees')
    #     user = fields.Many2many('res.users', string="User(s)")
    user = fields.Many2many('hr.employee', string="Employee(s)")

    @api.onchange('all_user')
    def user_auto(self):
        if not self.all_user == True:
            self.user = None
        if self.all_user == True:
            j = self.env['hr.employee'].search([])
            self.user = j

    def create_invoice(self):
        for order in self:
            invoice_line_ids = []
            if (order.start_date and order.end_date):
                invoice_line = []
                data_list = []

                account = self.env['account.account'].search([('name', '=', 'POSCommission')])
                employee_ids = self.env['hr.employee'].search([('id', 'in', order.user.ids)])
                for employee in employee_ids:
                    total_commission = 0

                    commission_data = self.env['commission.form'].search(
                        [('order_date', '>=', order.start_date), ('order_date', '<=', order.end_date),
                         ('active_employee', '=', employee.id), ('state', '=', 'done')])

                    if not commission_data:
                        raise UserError((
                                'No Record found against applied user: ' + employee.name + '\nKindly deselect all records not in done stage.'))
                    for data in commission_data:
                        #                         employee_partner = self.env['res.partner'].search([('name', '=', data.active_employee.name)])
                        if not data.active_employee.address_home_id:
                            raise UserError(
                                ('Partner of employee is not linked: ' + data.active_employee.name))

                        total_commission = total_commission + data.commission_amount
                        data.state = 'billed'

                    inv_obj = {
                        'partner_id': data.active_employee.address_home_id.id,
                        'invoice_date': fields.Date.today(),
                        'type': 'in_invoice',
                        'name': '/',
                        'state': 'draft',
                        'invoice_line_ids': [(0, 0, {'name': data.source_document,
                                                     'account_id': account.id,
                                                     'quantity': 1.0,
                                                     'price_unit': total_commission, })],
                    }

                    record = self.env['account.move'].create(inv_obj)