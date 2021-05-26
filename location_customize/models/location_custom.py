from odoo import fields, models, api, _
from lxml import etree

class location_stock(models.Model):
	_inherit = 'stock.location'

	# @api.model
	# def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
	# 	res = super(location_stock, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
	# 	doc = etree.XML(res['arch'])
	# 	for node in doc.xpath("//field[@name='transit_loc']"):
	# 		node.set('domain', str(self._transit_location()))
	# 		res['arch'] = etree.tostring(doc, encoding='unicode')
	# 	return res

	def _transit_location(self):
		for rec in self:
			locations = self.search([('usage','=','internal')])
			locations_in_trans = locations.mapped('transit_loc')
			trans_locations = self.search([('usage','=','transit')])
			locs = trans_locations - locations_in_trans
			rec.location_trans_ids = [(4, x) for x in locs.ids]

	location_trans_ids = fields.Many2many('stock.location', compute='_transit_location')
	transit_loc=fields.Many2one('stock.location',string="In-Transit Location")
