from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class SaleQuotation(models.Model):
    _inherit = 'sale.order'

    
    
    technical_representative = fields.Many2one('res.users', string="Technical Representative")
    customer = fields.Selection(selection=[('with tax', 'With Tax'),('without tax', 'Without Tax'),], default='with tax' , string="Print As")
#     local_vendor = fields.Boolean(string="Local", default=True)
#     foreign_vendor = fields.Boolean(string="Foreign")
    
#     quotation_ref = fields.Char(string="Quotation Reference")
    