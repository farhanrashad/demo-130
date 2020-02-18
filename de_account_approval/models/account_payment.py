# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountPaymentWHT(models.Model):
    _inherit = 'account.payment'
    
    state = fields.Selection([('draft', 'Draft'), ('waiting_approval', 'Waiting For Approval'), ('accountant_approved', 'Approved'), ('manager_approved', 'Approved'), ('rejected', 'Rejected'),('posted', 'Validated'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], tracking=True, readonly=True, default='draft', copy=False, string="Status",)
    
    
    def action_submit(self):
        self.write({
            'state':'waiting_approval',
        })
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'payment_id':self.id,
            'status':'Prepared By'
        })
        self.message_post(body=_('Payment has submitted by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
        
    def action_approve_accountant(self):
        self.write({
            'state':'accountant_approved',
        })
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'payment_id':self.id,
            'status':'Reviewed By'
        })
        self.message_post(body=_('Payment has reviewed by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
    
    def action_approve_manager(self):
        self.write({
            'state':'manager_approved',
        })
        self.post()
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'payment_id':self.id,
            'status':'Approved By'
        })
        self.message_post(body=_('Payment has approved and posted by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
        
    def action_reject(self):
        self.write({
            'state':'rejected',
            'approval_level':self.approval_level-1,
        })
        
    
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconcilable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:

            #if rec.state != 'draft':
                #raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'posted' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            moves = AccountMove.create(rec._prepare_payment_moves())
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

            # Update the state / move before performing any reconciliation.
            move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
            rec.write({'state': 'posted', 'move_name': move_name})

            if rec.payment_type in ('inbound', 'outbound'):
                # ==== 'inbound' / 'outbound' ====
                if rec.invoice_ids:
                    (moves[0] + rec.invoice_ids).line_ids \
                        .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id)\
                        .reconcile()
            elif rec.payment_type == 'transfer':
                # ==== 'transfer' ====
                moves.mapped('line_ids')\
                    .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id)\
                    .reconcile()

        return True
    
class AccountApprovalLog(models.Model):
    _name = 'account.approval.log'
    _description = 'Account Approval Log'
    
    user_id = fields.Many2one('res.users', string='User', index=True, readonly=True, tracking=2, default=lambda self: self.env.user,)
    payment_id = fields.Many2one('account.payment',string='Payment No.',readonly=True)
    status = fields.Char(string='Status',readonly=True)