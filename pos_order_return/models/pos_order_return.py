# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo.tools.translate import _
from odoo.tools import float_is_zero
from odoo import api, fields, models
from odoo.exceptions import UserError, Warning
import psycopg2

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    not_returnable = fields.Boolean('Not Returnable')

class PosOrder(models.Model):
    _inherit = 'pos.order'

    is_return_order = fields.Boolean(string='Return Order',copy=False)
    return_order_id = fields.Many2one('pos.order','Return Order Of',readonly=True,copy=False)
    return_status = fields.Selection([('-','Not Returned'),('Fully-Returned','Fully-Returned'),('Partially-Returned','Partially-Returned'),('Non-Returnable','Non-Returnable')],default='-',copy=False,string='Return Status')

    @api.model
    def _process_order(self, order, draft, existing_order):
    #-------- for order return code start-----------------
        data = order.get('data')
        if data.get('is_return_order'):
            data['amount_paid'] = 0
            for line in data.get('lines'):
                line_dict = line[2]
                line_dict['qty'] = line_dict['qty']
                if line_dict.get('original_line_id'):
                    original_line = self.env['pos.order.line'].browse(line_dict.get('original_line_id'))
                    original_line.line_qty_returned += abs(line_dict['qty'])
            for statement in data.get('statement_ids'):
                statement_dict = statement[2]
                if data['amount_total'] <0:
                    statement_dict['amount'] = statement_dict['amount'] * -1
                else:
                    statement_dict['amount'] = statement_dict['amount']
            if data['amount_total'] <0:
                data['amount_tax'] = data.get('amount_tax')
                data['amount_return'] = 0
                data['amount_total'] = data.get('amount_total')
    #----------  for order return code end  --------
        res = super(PosOrder,self)._process_order(order,draft, existing_order)
        return res

    @api.model
    def _order_fields(self,ui_order):
        fields_return = super(PosOrder,self)._order_fields(ui_order)
        fields_return.update({
            'is_return_order':ui_order.get('is_return_order') or False,
            'return_order_id':ui_order.get('return_order_id') or False,
            'return_status':ui_order.get('return_status') or False,
            })
        return fields_return

    def print_pos_receipt(self):
        output = []
        discount = 0
        order_id = self.search([('id', '=', self.id)], limit=1)
        # barcode_img = order_id.barcode_img
        client = order_id.partner_id.name or ''
        client_phone = order_id.partner_id.phone or ''
        name = order_id.pos_reference
        date_order = order_id.date_order
        orderlines = self.env['pos.order.line'].search([('order_id', '=', order_id.id)])
        payments = self.env['pos.payment'].search([('pos_order_id', '=', order_id.id)])
        note = order_id.note or ''
        paymentlines = []
        subtotal = 0
        tax = 0
        change = 0
        total_qty = sum(orderlines.mapped('qty'))
        orderlines
        for payment in payments:
            if payment.amount > 0:
                temp = {
                    'amount': payment.amount,
                    'name': payment.payment_method_id.name
                }
                paymentlines.append(temp)
            else:
                change += payment.amount
             
        for orderline in orderlines:
            new_vals = {
                'product_id': orderline.product_id.variant_name,
                'note': orderline.note,
                'total_price' : orderline.price_subtotal_incl,
                'qty': orderline.qty,
                'price_unit': orderline.price_unit,
                'discount': orderline.discount,
                'tax_total': sum(orderline.tax_ids.mapped('amount')),
                'promo_discount': (orderline.price_unit * orderline.qty) - orderline.price_subtotal,
            }

            # if orderline.discount_line_type == 'percentage' :
            #     discount += orderline.price_unit*(orderline.discount/100)*orderline.qty

            # else :
            #     discount += orderline.discount * orderline.qty
            
            # discount += (orderline.price_unit * orderline.qty * orderline.discount) / 100
            # subtotal +=orderline.price_subtotal
            # tax += (orderline.price_subtotal_incl - orderline.price_subtotal)
            discount += new_vals['promo_discount']
            subtotal +=orderline.price_subtotal
            tax += (orderline.price_subtotal_incl - orderline.price_subtotal)
            output.append(new_vals)
        print('>>>>>>>>>.', discount)
        return [output, discount, paymentlines, change, subtotal, tax, client, client_phone, total_qty, note]


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    line_qty_returned = fields.Integer('Line Returned', default=0)
    original_line_id = fields.Many2one('pos.order.line', "Original line")

    @api.model
    def _order_line_fields(self,line,session_id=None):
        fields_return = super(PosOrderLine,self)._order_line_fields(line,session_id)
        fields_return[2].update({'line_qty_returned':line[2].get('line_qty_returned','')})
        fields_return[2].update({'original_line_id':line[2].get('original_line_id','')})
        return fields_return
