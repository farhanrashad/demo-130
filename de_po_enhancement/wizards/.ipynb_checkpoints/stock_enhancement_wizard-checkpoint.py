from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPickingWizard(models.Model):
    _name = "stock.enhancement"
    _description = "Stock Picking Wizard"

    products_sp = fields.Char(string='Products')
    demand_sp = fields.Float(string='Demand')
    quantity_sp = fields.Float(string='Quantity Done')
    stock_pick = fields.One2many('stock.enhancement.line', 'stock_order_ids')
    ps_line_id = fields.Many2one('stock.move')
    ps_line_ref = fields.Integer()
    
    @api.model
    def create(self,vals):
        res = super(StockPickingWizard,self).create(vals)
        res.ps_line_id = res.ps_line_ref
        res.ps_line_id.check_id_stock = res.id
#         raise UserError(res.po_line_id.id)
        return res

class StockPickingWizardLine(models.Model):
    _name = "stock.enhancement.line"
    _description = "Stock Picking Wizard Line"

    stock_order_ids = fields.Many2one('stock.enhancement')

    sale_order_sp = fields.Many2one('sale.order', string='SO')
    quantity = fields.Char(string='Quantity')


# class StockMoveLineInherit(models.Model):
#     _inherit = 'stock.move'

#     @api.onchange('products_sp', 'quantity_sp')
#     def get_quantity(self):
#         model = self.env.context.get('active_model')
#         rec = self.env[model].browse(self.env.context.get('active_id'))
#         for line in rec:
#             line.product_id = self.products_sp

#             line.product_qty = self.quantity_sp
