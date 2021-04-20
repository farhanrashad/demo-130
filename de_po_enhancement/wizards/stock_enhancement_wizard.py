from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPickingWizard(models.Model):
    _name = "stock.enhancement.wizard"
    _description = "Stock Picking Wizard"

    products_sp = fields.Char(string='Products')
    demand_sp = fields.Float(string='Demand')
    quantity_sp = fields.Float(string='Quantity Done')

    stock_pick = fields.One2many('stock.enhancement.line.wizard', 'stock_order_ids')


class StockPickingWizardLine(models.Model):
    _name = "stock.enhancement.line.wizard"
    _description = "Stock Picking Wizard Line"

    stock_order_ids = fields.Many2one('stock.enhancement.wizard')

    sale_order_po = fields.Many2one('sale.order', string='SO')
    quantity = fields.Char(string='Quantity')


class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move'

    @api.onchange('products_po', 'quantity_po')
    def get_quantity(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        for line in rec:
            line.product_id = self.products_po

            line.product_qty = self.quantity_po
