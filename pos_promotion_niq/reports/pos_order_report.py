# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    _description = "Point of Sale Orders Statistics"

    price_total_with_tax = fields.Float(string='Total with Tax', readonly=True)
    price_total_without_tax = fields.Float(string='Total w/o Tax', readonly=True)
    total_promo_disc_percentage = fields.Float(string='Disc %', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + """
        ,l.promo_disc_percentage as total_promo_disc_percentage
        ,SUM(
          CASE
              WHEN (l.discount > 0 OR l.promo_disc_percentage > 0)
                  THEN (l.qty * l.price_unit * (100 - l.discount) / 100 * (100 - COALESCE(l.promo_disc_percentage, 0))/100)
              ELSE
                  (l.qty * l.price_unit)
          END) AS price_total_without_tax
        ,SUM((l.qty * l.price_subtotal_incl) * (100 - l.discount) / 100 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) AS price_total_with_tax
        """

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',l.promo_disc_percentage'
