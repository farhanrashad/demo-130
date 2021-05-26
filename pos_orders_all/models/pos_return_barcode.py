# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, tools
import random
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

class PosBarcode(models.Model):
	_inherit = 'pos.order'

	barcode = fields.Char(string='Barcode')
	barcode_img = fields.Binary('Order Barcode Image')

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
		res = super(PosBarcode, self)._order_fields(ui_order)
		process_line = partial(self.env['pos.order.line']._order_line_fields, session_id=ui_order['pos_session_id'])
		res['barcode'] = ui_order['barcode']
		res['barcode_img'] = ui_order['barcode_img']
		return res
