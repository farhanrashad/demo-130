from odoo import fields, models, api, _
from lxml import etree

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	def _total_items(self):
		for pick in self:
			pick.total_items = len(pick.move_lines.mapped('product_id'))

	total_items = fields.Integer('Total Items', compute='_total_items')

class StockMove(models.Model):
	_inherit = 'stock.move'

	barcode = fields.Char('Barcode', copy=False, help="International Article Number used for product identification.")

	@api.onchange('product_id', 'product_qty')
	def onchange_quantity(self):
		res = super(StockMove, self).onchange_quantity()
		if self.product_id:
			self.barcode  = self.product_id.barcode
		return res

	@api.onchange('product_id')
	def onchange_product_id(self):
		res = super(StockMove, self).onchange_product_id()
		if self.product_id:
			self.barcode  = self.product_id.barcode
		return res

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    barcode = fields.Char(related="product_id.barcode", store=True)

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    barcode = fields.Char(related="product_id.barcode", store=True)


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    barcode = fields.Char()

    def _select(self):
        return super(PosOrderReport, self)._select() + ",p.barcode"


    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ",p.barcode"

class StockRule(models.Model):
	_inherit = 'stock.rule'

	def _push_prepare_move_copy_values(self, move_to_copy, new_date):
		res = super(StockRule, self)._push_prepare_move_copy_values(move_to_copy=move_to_copy,new_date=new_date)
		res.update({'barcode': move_to_copy.product_id.barcode})
		return res
