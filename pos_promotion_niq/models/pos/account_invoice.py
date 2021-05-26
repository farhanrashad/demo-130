# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _prepare_line(self, order_line):
        res = super(PosSession, self)._prepare_line(order_line)
        sign = -1 if order_line.qty >= 0 else 1
        new_price_unit = order_line.compute_unit_price()
        price = sign * new_price_unit
        tax_ids = order_line.tax_ids_after_fiscal_position\
                    .filtered(lambda t: t.company_id.id == order_line.order_id.company_id.id)
        if self.company_id.tax_calculation_rounding_method == 'round_globally':
            is_refund = all(line.qty < 0 for line in order_line.order_id.lines)
        else:
            is_refund = order_line.qty < 0
        taxes = tax_ids.compute_all(price_unit=price, quantity=abs(order_line.qty), currency=self.currency_id, is_refund=is_refund).get('taxes', [])
        date_order = order_line.order_id.date_order
        taxes = [{'date_order': date_order, **tax} for tax in taxes]
        res['taxes'] = taxes
        return res

class AccountMove(models.Model):

    _inherit = 'account.move'
    # def _create_account_move_line(self, session=None, move=None):
    #     self = self.with_context(pos_promotion_niq=True)
    #     return super(PosOrder, self)._create_account_move_line(session, move)

    # def _register_hook(self):
    #     def action_get_taxes_values(self):
    #         tax_grouped = {}
    #         round_curr = self.currency_id.round
    #         for line in self.invoice_line_ids:
    #             if not line.account_id:
    #                 continue
    #             # hack here to recompute taxes base on new promotion config
    #             # price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
    #             price_unit = line.compute_unit_price()
    #             taxes = line.invoice_line_tax_ids.compute_all(
    #                 price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
    #             for tax in taxes:
    #                 val = self._prepare_tax_line_vals(line, tax)
    #                 key = self.env['account.tax'].browse(
    #                     tax['id']).get_grouping_key(val)

    #                 if key not in tax_grouped:
    #                     tax_grouped[key] = val
    #                     tax_grouped[key]['base'] = round_curr(val['base'])
    #                 else:
    #                     tax_grouped[key]['amount'] += val['amount']
    #                     tax_grouped[key]['base'] += round_curr(val['base'])
    #         return tax_grouped
    #     self._patch_method("get_taxes_values",
    #                        action_get_taxes_values)
