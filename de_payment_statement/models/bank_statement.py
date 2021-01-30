from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    bank_statement_entry = fields.Boolean(string='Add Bank Statement Entry')
    bank_statement = fields.Many2one('res.bank')
    bank_statement_partner = fields.Many2one('res.partner.bank')
