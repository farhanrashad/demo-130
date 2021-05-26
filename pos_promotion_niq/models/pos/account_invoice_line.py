# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    promo_disc_percentage = fields.Float('Disc %')
    promo_disc_amount = fields.Float('Disc Amount')
    promo_fixed_price = fields.Float('Fixed Price')
    promo_get_free = fields.Boolean('Free')

    def compute_unit_price(self):
        self.ensure_one()
        line = self
        new_price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        if line.promo_disc_percentage or \
                line.promo_disc_amount or \
                line.promo_fixed_price or \
                line.promo_get_free:
            if line.promo_disc_percentage:
                new_price_unit = line.price_unit * \
                    (1 - (line.discount or 0.0) / 100.0) * \
                    (1 - (line.promo_disc_percentage or 0.0) / 100.0)
            if line.promo_disc_amount or line.promo_get_free:
                new_price_unit = line.price_unit - line.promo_disc_amount
            if line.promo_fixed_price:
                new_price_unit = line.promo_fixed_price
        return new_price_unit

    # def _register_hook(self):
    #     @api.depends(
    #         'price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
    #         'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
    #         'invoice_id.date_invoice', 'invoice_id.date')
    #     def _compute_price(self):
    #         currency = self.invoice_id and self.invoice_id.currency_id or None
    #         price = self.compute_unit_price()
    #         taxes = False
    #         if self.invoice_line_tax_ids:
    #             taxes = self.invoice_line_tax_ids.compute_all(
    #                 price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
    #         self.price_subtotal = price_subtotal_signed = taxes[
    #             'total_excluded'] if taxes else self.quantity * price
    #         self.price_total = taxes['total_included'] if taxes else self.price_subtotal
    #         if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
    #             currency = self.invoice_id.currency_id
    #             date = self.invoice_id._get_currency_rate_date()
    #             price_subtotal_signed = currency._convert(
    #                 price_subtotal_signed, self.invoice_id.company_id.currency_id, self.company_id or self.env.user.company_id, date or fields.Date.today())
    #         sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
    #         self.price_subtotal_signed = price_subtotal_signed * sign

    #     self._patch_method("_compute_price",
    #                        _compute_price)
