# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class PosOrderLine(models.Model):

    _inherit = 'pos.order.line'

    origin_price = fields.Float('Origin Price')
    promo_disc_percentage = fields.Float('Disc %')
    promo_disc_amount = fields.Float('Disc Amount')
    promo_fixed_price = fields.Float('Fixed Price')
    promo_get_free = fields.Boolean('Free')
    promotion_id = fields.Many2one('pos.promotion', 'Pos Promotion')

    @api.depends('price_unit', 'tax_ids', 'qty', 'discount',
                 'promo_disc_percentage', 'promo_disc_amount',
                 'promo_fixed_price', 'product_id')
    def _compute_amount_line_all(self):

        super(PosOrderLine, self)._compute_amount_line_all()

        for line in self:
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

                fpos = line.order_id.fiscal_position_id
                tax_ids_after_fiscal_position = fpos.map_tax(
                    line.tax_ids, line.product_id, line.order_id.partner_id) \
                    if fpos else line.tax_ids
                taxes = tax_ids_after_fiscal_position.compute_all(
                    new_price_unit, line.order_id.pricelist_id.currency_id,
                    line.qty, product=line.product_id,
                    partner=line.order_id.partner_id)
                line.update({
                    'price_subtotal_incl': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })

    def compute_unit_price(self):
        self.ensure_one()
        line = self
        new_price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        if line.promo_disc_percentage or \
                line.promo_disc_amount or \
                line.promo_fixed_price or \
                line.promo_get_free:
            if line.promo_disc_percentage:
                new_price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * (1 - (line.promo_disc_percentage or 0.0) / 100.0)
            if line.promo_disc_amount or line.promo_get_free:
                new_price_unit = line.price_unit - line.promo_disc_amount
            if line.promo_fixed_price:
                new_price_unit = line.promo_fixed_price
        return new_price_unit