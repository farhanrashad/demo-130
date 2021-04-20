from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrderWizard(models.Model):
    _name = "purchase.enhancement.wizard"
    _description = "PO Wizard"

    products_po = fields.Char(string='Products')
    demand_po = fields.Float(string='Demand')
    quantity_po = fields.Float(string='Quantity Done')

    purchase_order = fields.One2many('purchase.enhancement.line.wizard', 'purchase_order_ids')


class PurchaseOrderWizardLine(models.Model):
    _name = "purchase.enhancement.line.wizard"
    _description = "PO Wizard Line"

    purchase_order_ids = fields.Many2one('purchase.enhancement.wizard')

    sale_order_po = fields.Many2one('sale.order', string='SO')
    quantity = fields.Char(string='Quantity')


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('products_po', 'quantity_po')
    def get_quantity(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        for line in rec:
            line.product_id = self.products_po

            line.product_qty = self.quantity_po
