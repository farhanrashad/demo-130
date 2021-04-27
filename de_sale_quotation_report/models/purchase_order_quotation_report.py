from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class PurchaseQuotationReport(models.Model):
    _inherit = 'purchase.order'

    
    
    vendor_name = fields.Many2one('res.partner', string="Foreign Customers")
    local_vendor = fields.Boolean(string="Local", default=True)
    foreign_vendor = fields.Boolean(string="Foreign")
    cutomers = fields.Selection(selection=[('local_vendor', 'Local'),('foreign_vendor', 'Foreign'),], default='local_vendor' , string="Vendor")
    quotation_ref = fields.Char(string="Quotation Reference")
    