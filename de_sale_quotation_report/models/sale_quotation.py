from odoo import api, fields, models



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tech_rep = fields.Many2one('res.users', string="Technical Representative")
