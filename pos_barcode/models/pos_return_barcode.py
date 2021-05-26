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
    return_id = fields.Many2one('pos.order', string="Return Of")

    @api.model
    def create(self, vals):
        order_id = super(PosBarcode, self).create(vals)
        return_id = order_id.return_id
        if return_id:
            for line in order_id.lines:
                return_line = return_id.lines.filtered(lambda x: x.product_id.id == line.product_id.id)
                return_line.return_qty += -line.qty
        return order_id

    @api.model
    def get_return_data(self, order_id, name):
        return_id = False
        if order_id:
            return_id = self.search([('id', '=', order_id)], limit=1).return_id
        else:
            return_id = self.search([('name', '=', name)], limit=1).return_id
        return return_id.id

    @api.model
    def set_return_qty(self, order_id, name):
        return_qty = 0.0
        if order_id:
            orders = self.env['pos.order'].search([('return_id', '=', int(order_id))])
            return_qty = sum(orders.mapped('lines.qty'))
        else:
            return_qty = sum(orders.mapped('lines.qty'))
        return return_qty

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
        if 'return_id' in ui_order:
            res['return_id'] = ui_order['return_id']
        return res

    def return_new_order(self):
        lines = []
        for ln in self.lines:
            lines.append(ln.id)
        vals = {
            'amount_total': self.amount_total,
            'date_order': self.date_order,
            'id': self.id,
            'name': self.name,
            'partner_id': [self.partner_id.id, self.partner_id.name] if self.partner_id else '',
            'pos_reference': self.pos_reference,
            'state': self.state,
            'session_id': [self.session_id.id, self.session_id.name],
            'company_id': [self.company_id.id, self.company_id.name],
            'lines': lines,
            'order_lines': self.return_new_order_line(),
            'amount_tax':self.amount_tax,
            'barcode': self.barcode,
        }
        return vals
    
    def return_new_order_line(self):
        orderlines = self.env['pos.order.line'].search([('order_id.id','=', self.id)])
        final_lines = []
        for line in orderlines:
            vals = {
                'discount': line.discount,
                'id': line.id,
                'order_id': [line.order_id.id, line.order_id.name],
                'price_unit': line.price_unit,
                'product_id': [line.product_id.id, line.product_id.display_name],
                'qty': line.qty,
            }
            final_lines.append(vals)
        return final_lines   

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    return_qty = fields.Float('Return Quantity', digits='Product Unit of Measure')

    @api.model
    def set_return_qty(self, lines):
        line_ids = self.browse([int(key) for key in list(lines)])
        for line in line_ids:
          line.return_qty += lines[str(line.id)]
