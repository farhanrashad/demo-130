from odoo import models, fields, api


class AdvancePayment(models.Model):
    _name = 'advance.payment'

    payment_date = fields.Datetime(string='Payment', index=True)
    partner_id = fields.Many2one('res.partner')
    amount = fields.Integer('Payment Amount')
    payment_method_id = fields.Many2one('account.payment')
    journal_id = fields.Many2one('account.journal')
#     memo = fields.Char('Memo')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('reconsile', 'Reconsiled'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
