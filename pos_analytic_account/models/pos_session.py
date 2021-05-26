# -*- coding: utf-8 -*-

from odoo import models, fields


class PosSession(models.Model):
    _inherit = 'pos.session'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        related="config_id.account_analytic_id",
        store=True, string='Analytic Account', copy=False
    )

    def _prepare_line(self, order_line):
        res = super(PosSession, self)._prepare_line(order_line)
        res['analytic_account_id'] = order_line.order_id.account_analytic_id or False
        return res

    def _get_combine_receivable_vals(self, payment_method, amount, amount_converted):
        res = super(PosSession, self)._get_combine_receivable_vals(payment_method, amount, amount_converted)
        res['analytic_account_id'] = self.account_analytic_id.id or False
        return res

    def _get_tax_vals(self, key, amount, amount_converted, base_amount_converted):
        res = super(PosSession, self)._get_tax_vals(key, amount, amount_converted, base_amount_converted)
        res['analytic_account_id'] = self.account_analytic_id.id or False
        return res

    def _get_sale_vals(self, key, amount, amount_converted):
        res = super(PosSession, self)._get_sale_vals(key, amount, amount_converted)
        res['analytic_account_id'] = self.account_analytic_id.id or False
        return res

    # def _get_stock_output_vals(self, out_account, amount, amount_converted):
    #     res = super(PosSession, self)._get_stock_output_vals(out_account, amount, amount_converted)
    #     res['analytic_account_id'] = self.account_analytic_id.id or False
    #     return res

    def _get_stock_expense_vals(self, exp_account, amount, amount_converted):
        res = super(PosSession, self)._get_stock_expense_vals(exp_account, amount, amount_converted)
        res['analytic_account_id'] = self.account_analytic_id.id or False
        return res

    def _get_rounding_difference_vals(self, amount, amount_converted):
        res = super(PosSession, self)._get_rounding_difference_vals(amount, amount_converted)
        res['analytic_account_id'] = self.account_analytic_id.id or False
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def create(self, vals):
        res = super(AccountMoveLine, self).create(vals)
        if res.statement_id and res.statement_id.pos_session_id and res.statement_id.pos_session_id.account_analytic_id:
            res.analytic_account_id = res.statement_id.pos_session_id.account_analytic_id.id
        return res
