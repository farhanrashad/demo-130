# -*- coding: utf-8 -*-
# Part of Dynexcel. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class SaleOrderWizard(models.TransientModel):
	_name = 'sale.order.wizard'
	_description = "Sale Order Wizard"

	order_line_ids = fields.One2many( 'sale.order.line.wizard', 'order_id',String="Order Line")
	partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
	date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)


	def action_create_sale_order(self):
		self.ensure_one()
		res = self.env['sale.order'].browse(self._context.get('id',[]))
		value = []
		pricelist = self.partner_id.property_product_pricelist
		partner_pricelist = self.partner_id.property_product_pricelist

		for data in self.order_line_ids:
			if partner_pricelist:
				product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=data.product_uom.id)
				final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_qty or 1.0, self.partner_id)
			
			else:
				final_price = data.product_id.standard_price
			 	
			value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'date_planned' : data.date_planned,
								'price_unit' : final_price,
								}])
			print('####################################3',value)
		res.create({
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,
						
					})
		
		return res


class SaleOrderLineWizard(models.TransientModel):
	_name = 'sale.order.line.wizard'
	_description = "Sale Order Line Wizard"

	order_id = fields.Many2one('sale.order.wizard')
		
	product_id = fields.Many2one('product.product', string="Product", required=True)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantity', required=True)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit
