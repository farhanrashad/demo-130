from odoo import api, fields, models
from odoo.exceptions import UserError


class QuantativeBudgetPurchaseAgreement(models.Model):
    _inherit = 'purchase.requisition'
    
    name = fields.Char(string="Name")
    subject = fields.Char(string="Subject")
    budget = fields.Many2one('crossovered.budget', string="Budget")

    def _current_user(self):
        user = self.env.user
        self.requester = user


class QuantativeBudgetPurchaseAgreementLine(models.Model):
    _inherit = 'purchase.requisition.line'

    analytic_acc = fields.Char(string="Analytic Account")
    budgetary_position = fields.Many2one('account.budget.post', string="Budgetary Position")
    analytic_tag = fields.Many2one('account.analytic.account', string="Analytic Tag")
    unit_price = fields.Float(string="Unit Price")
    tax = fields.Float(string="Taxes")
    subtotal = fields.Float(string="Subtotal")
