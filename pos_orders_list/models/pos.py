# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import Warning
import random
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)
try:
	import barcode
except ImportError :
	_logger.debug('Cannot `import barcode` please run this command: sudo pip3 install python-barcode')

try:            
	from barcode.writer import ImageWriter
except ImportError:
	ImageWriter = None

import base64
import os
from functools import partial




class pos_order(models.Model):
	_inherit = 'pos.order'

	pos_order_date = fields.Date('Oder Date', compute='get_order_date')
	barcode = fields.Char(string="Order Barcode")
	barcode_img = fields.Binary('Order Barcode Image')

	def get_order_date(self):
		for i in self:
			is_dt = i.date_order.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
			d1= datetime.strptime(is_dt,DEFAULT_SERVER_DATETIME_FORMAT).date()
			i.pos_order_date = d1


	def get_barcode(self,brcd):
		code = (random.randrange(1111111111111,9999999999999))
		bcode = self.env['barcode.nomenclature'].sanitize_ean("%s" % (code))
		pos_order = self.env['pos.order'].search([])
		for i in pos_order:
			if i.barcode  == bcode:
				code = (random.randrange(1111111111111,9999999999999))
				bcode = self.env['barcode.nomenclature'].sanitize_ean("%s" % (code))
		if ImageWriter != None:
			encode = barcode.get('ean13', bcode, writer=ImageWriter())
			if os.path.exists("/tmp"):
				filename = encode.save('/tmp/ean13')
			else:
				filename = encode.save('ean13')
			if os.path.exists(filename):
				file = open(filename, 'rb')
				jpgdata = file.read()
				imgdata = base64.encodestring(jpgdata)
				os.remove(filename) 
				return [bcode,imgdata]


	@api.model
	def _order_fields(self, ui_order):
		res = super(pos_order, self)._order_fields(ui_order)
		process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
		res['barcode'] = ui_order['barcode']
		res['barcode_img'] = ui_order['barcode_img']
		return res

	

class pos_config(models.Model):
	_inherit = 'pos.config'
	
	show_order = fields.Boolean('Show Orders')
	pos_session_limit = fields.Selection([('all',  "Load all Session's Orders"), ('last3', "Load last 3 Session's Orders"), ('last5', " Load last 5 Session's Orders"),('current_day', "Only Current Day Orders"), ('current_session', "Only Current Session's Orders")], string='Session limit',default="current_day")
	show_barcode = fields.Boolean('Show Barcode in Receipt')
	show_draft = fields.Boolean('Show Draft Orders')
	show_posted = fields.Boolean('Show Posted Orders')

