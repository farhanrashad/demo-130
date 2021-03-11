from odoo import fields, models, _


class ForecastStock(models.Model):
    _inherit = 'product.template'

    forecast_stock=fields.Float(string='Forecast on Stock', compute='compute_forecast_stock')
    #
    def compute_forecast_stock(self):
        self.forecast_stock =100
    #     """
    #     To get Count against SO for Different PO
    #     """
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'binding_type': 'action',
    #         'name': 'Purchase Order',
    #         'res_model': 'purchase.order',
    #         'domain': [('sale_order_id', '=', self.id)],
    #         'target': 'current',
    #         'view_mode': 'tree,form',
    #     }
    #
    # def compute_forecast_stock(self):
    #     for record in self:
    #         record.forecast_stock = 100
    #
    #         # record.forecast_stock = self.env['purchase.order'].search_count(
    #         #     [('sale_order_id', '=', self.id)])