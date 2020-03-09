from odoo import models, fields, api, _

class Saleorderstatus(models.Model):
    _inherit = 'sale.order'

    sale_order_status = fields.Selection([('in-process', 'In-process'),
                                    ('shipped', 'Shipped'),
                                    ('pending', 'Pending'),
                                    ('cancelled', 'Cancelled'),
                                    ], default='in-process', string='Status')