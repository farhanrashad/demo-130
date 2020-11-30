from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PosCommissionRule(models.Model):
    _name = 'pos.commission.rule'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'name'

    name = fields.Char(required=True)
    apply_on = fields.Selection([('pos', 'Pos Order')], 'Apply On', default="pos")
    priority = fields.Integer("Priority", default="1")
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    minimum_order = fields.Float("Minimum Order")
    rule_line = fields.One2many("pos.commission.beneficiary", "rule_order")
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
                    'employee_id': employee.id,
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
                emp_list.append(line.employee_id.id)

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
        rules = super(PosCommissionRule, self).create(values)
        return rules

    def write(self, values):
        emp_list = []
        if self.rule_line:
            for line in self.rule_line:
                emp_list.append(line.employee_id.id)

        employees = self.env['hr.employee'].search([('id', 'in', emp_list)])

        for employee in employees:
            employee.update({
                'employee_set': True,
            })
        rules = super(PosCommissionRule, self).write(values)
        return rules


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    employee_set = fields.Boolean()


class PosCommissionBeneficiary(models.Model):
    _name = 'pos.commission.beneficiary'

    employee_id = fields.Many2one('hr.employee', string="Employee", domain=[('employee_set', '=', False)], required=True)
    job_position = fields.Many2one(related='employee_id.job_id')
    compute_price = fields.Selection([('percentage', 'Percentage')], default='percentage', readonly=True)
    commission_price = fields.Float("Commission(%)")
    rule_order = fields.Many2one("pos.commission.rule")

    @api.onchange('employee_id')
    def onchange_production_order(self):
        if self.employee_id:
            employee_names = self.env['hr.employee'].search([('name', '=', self.employee_id.name)])
            for employee_name in employee_names:
                employee_name.update({
                    'employee_set': True,
                })
