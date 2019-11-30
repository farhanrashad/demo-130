# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp


class SalesWarrenty(models.Model):
    _name = 'sales.warranty'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Sale Warranty'
    _order = 'id desc'
    
    name = fields.Char(string='Name',  copy=False,  index=True, default=lambda self: _('New'))
    internal_reference = fields.Text(string='Internal Reference')
    product_id = fields.Many2one('product.product',string='Product', track_visibility='onchange')
    sno = fields.Char(string='Serial No',track_visibility='onchange')
    customer_id = fields.Many2one('res.partner',string='Customer', track_visibility='onchange')
    sale_id = fields.Many2one('sale.order', string='SO Reference')
    invoice_id = fields.Many2one('account.invoice',string='Invoice Reference')
    purchase_date = fields.Date(string='Date of Purchase')
    warranty_end_date = fields.Date(string='Warranty End Date',track_visibility='onchange')
    state = fields.Selection([('inwarranty','In Warranty'),
                              ('toexpire','To Expire'),
                              ('expired','Expired')],string = "Status", default='inwarranty',track_visibility='onchange')