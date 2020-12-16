from odoo import models, api, fields


class PosRepeatOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_lines(self, ref):
        """To get the values of the corresponding order"""
        result = []
        order_id = self.search([('pos_reference', '=', ref)], limit=1)
        if order_id:
            lines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
            for line in lines:
                new_vals = {
                    'product_id': line.product_id.id,
                    'product': line.product_id.name,
                    'qty': line.qty,
                    'price_unit': (-1)*line.price_unit,
                    'discount': line.discount,
                    'line_id': line.id,
                }
                result.append(new_vals)

        return [result]
