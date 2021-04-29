from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class ContactBankIban(models.Model):
    _inherit = 'res.bank'

    iban = fields.Char(string="IBAN#")
    note_line = fields.Char(string="Note Line")
    swift = fields.Char(string="Swift Code")
    
        
    
class ContactBankNtnGst(models.Model):
    _inherit = 'res.company'

    ntn = fields.Char(string="NTN")
    gst = fields.Char(string="GST")
    
    
    
class AccountMoveInvoice(models.Model):
    _inherit = 'account.move'
    
    dispatch_date =  fields.Date(string="Dispatch Date" , default=date.today())
    dispatch_via = fields.Char(string="Dispatch Via")
    commercial_sales_invoice = fields.Selection(selection=[('commercial', 'Commercial'),('sales_tax', 'Sales Tax'),], default='commercial' ,string="Invoice")
    
    bank_id = fields.Many2one('res.bank',string="Banks")
    bank = fields.Many2one('res.partner.bank',string="Banks")
    
    
    
#     def find_qty(self):
#         est_qty = self.env['purchase.order'].search([])
#         for record in est_qty.order_line:
#             raise UserError(record.product_qty)
            





