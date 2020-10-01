from odoo import models, fields, api


class DiscountInvoices(models.Model):
    _inherit = 'account.move'

    discount = fields.Float()

    @api.onchange('discount')
    def discount_invoice(self):
        self.amount_total = self.amount_untaxed - self.discount

