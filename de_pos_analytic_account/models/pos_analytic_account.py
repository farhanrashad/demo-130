from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_is_zero


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account")


class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    analytic_account = fields.Char('account.analytic.account')


class PosPaymentInherit(models.Model):
    _inherit = 'pos.payment'

    analytic_account = fields.Many2one('account.analytic.account')


class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    #     def _create_account_move(self):

    #         res = super(PosSessionInherit, self)._create_account_move()
    # #         res = self.env['account.move'].search()  res.move_id
    #         res['account_move']
    #         return res

    def _create_account_move(self):
        journal = self.config_id.journal_id
        # Passing default_journal_id for the calculation of default currency of account move
        # See _get_default_currency in the account/account_move.py.
        account_move = self.env['account.move'].with_context(default_journal_id=journal.id).create({
            'journal_id': journal.id,
            'date': fields.Date.context_today(self),
            'ref': self.name,
        })
        self.write({'move_id': account_move.id})

        data = {}
        data = self._accumulate_amounts(data)
        data = self._create_non_reconciliable_move_lines(data)
        data = self._create_cash_statement_lines_and_cash_move_lines(data)
        data = self._create_invoice_receivable_lines(data)
        data = self._create_stock_output_lines(data)
        data = self._create_extra_move_lines(data)
        data = self._reconcile_account_move_lines(data)

        for line in account_move.line_ids:
            line.update({
                'analytic_account_id': self.config_id.analytic_account.id,
            })


class PosOrderInherit(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        session = self.env['pos.session'].search([('id', '=', self.session_id.id)])

        return {
            'amount': ui_paymentline['amount'] or 0.0,
            'payment_date': ui_paymentline['name'],
            'payment_method_id': ui_paymentline['payment_method_id'],
            'card_type': ui_paymentline.get('card_type'),
            'transaction_id': ui_paymentline.get('transaction_id'),
            'pos_order_id': order.id,
            'analytic_account': order.session_id.config_id.analytic_account.id,
        }