from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PosCommission(models.Model):
    _name = 'pos.commission'
    _description = 'Commission records'
    _order = 'order_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    source_document = fields.Char("Source Document", readonly=True)
    user_id = fields.Many2one('res.users', string="User", readonly=True)
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
