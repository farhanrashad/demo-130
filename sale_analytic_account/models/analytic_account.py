# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    use_invoice = fields.Boolean(string="Use in Customer Invoice", copy=False,)

    @api.constrains('use_invoice')
    def _validate_use_invoice(self):
        if self.search_count([('use_invoice', '=', True)]) > 1:
            raise ValidationError(_('You cannot use more than one analytic account !'))

# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'

#     @api.model
#     def default_get(self, default_fields):
#         res = super(AccountMoveLine, self).default_get(default_fields)
#         analytic_account_id = self.env['account.analytic.account'].search([('use_invoice', '=', True)], limit=1)
#         if analytic_account_id and self.env.context.get('active_model') in ('sale.order', 'sale.advance.payment.inv'):
#             res['analytic_account_id'] = analytic_account_id and analytic_account_id.id
#         return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, default_fields):
        res = super(SaleOrder, self).default_get(default_fields)
        analytic_account_id = self.env['account.analytic.account'].search([('use_invoice', '=', True)], limit=1)
        if analytic_account_id:
            res['analytic_account_id'] = analytic_account_id.id
        return res

    def _create_invoices(self, grouped=False, final=False):
        res = super(SaleOrder, self)._create_invoices(grouped=False, final=False)
        analytic_account_id = self.env['account.analytic.account'].search([('use_invoice', '=', True)], limit=1)
        todo_lines = res.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable') and not line.analytic_account_id)
        todo_lines.write({'analytic_account_id': analytic_account_id.id})
        return res
