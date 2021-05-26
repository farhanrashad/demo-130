from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.depends('product_tmpl_id')
    def _compute_category_id(self):
    	for quant in self:
    		quant.category_id = quant.product_tmpl_id.categ_id

    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', string='Product Template', store=True)

    category_id = fields.Many2one('product.category', compute='_compute_category_id', string='Product Category', store=True)

