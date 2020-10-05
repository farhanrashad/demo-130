# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_charge = fields.Boolean(string='Is Charge', store=True)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    cost_lines = fields.One2many('mrp.production.direct.cost', 'production_id' ,string='Direct Cost Lines')    
    
    
class MrpCost(models.Model):
    _name = 'mrp.production.direct.cost'
    _description = 'This Production Order Cost'

    product_id = fields.Many2one('product.product',string='Product')
    production_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    is_charge = fields.Boolean(related='product_id.is_charge')
    standard_price = fields.Float(related='product_id.standard_price', readonly=False)
    is_billed = fields.Boolean(string='Billed')
    partner_id = fields.Many2one('res.partner', string='Vendor', default='product_id.seller_ids.name')
    

