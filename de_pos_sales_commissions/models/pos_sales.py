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
            rules = self.env['pos.commission.rule'].search([])
            for rule in rules:
                if str(rule.start_date) <= values['date_order'].split()[0] and str(rule.end_date) >= \
                        values['date_order'].split()[0]:

                    rule_records = self.env['pos.commission.rule'].search([('id', '=', rule.id), ('state', '=', 'lock')])
                    if values['amount_total'] >= rule_records.minimum_order:
                        for line in rule_records.rule_line:
                            if line.employee_id.id == values['employee_id']:
                                self.env['pos.commission'].create({
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
                commission_rules = self.env['pos.commission.rule'].search([])
                for commission_rule in commission_rules:
                    if commission_rule.start_date <= self.date_order.date() and commission_rule.end_date >= self.date_order.date():
                        rules = self.env['pos.commission.rule'].search([('id', '=', commission_rule.id)])
                        if self.amount_total >= rules.minimum_order:
                            for rule in rules.rule_line:
                                self.env['pos.commission'].create({
                                    'source_document': self.name,
                                    'User': rule.users_id.id,
                                    'order_date': self.date_order.date(),
                                    'sales_amount': self.amount_total,
                                    'commission_amount': ((rule.commission_price / 100) * self.amount_total),
                                    'pos_order': self.id,
                                    'payment_id': self.payment_ids.id,
                                })


class pos_order_line(models.Model):
    _name = 'pos.sale.commission'

    psl_order = fields.Many2one("pos.order")
    User = fields.Many2one('res.users', string="User")
    job_position = fields.Many2one('hr.job', string="Job Position")
    commission_amount = fields.Float("Commission Amount")


