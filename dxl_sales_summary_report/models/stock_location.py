# -*- coding: utf-8 -*-
from odoo import fields, models, api, _ , tools


class StockLocation(models.Model):
	_inherit = "stock.location"

	shop_id = fields.Many2one('pos.multi.shop', string="Shop")
