# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests
import json

class PosConfig(models.Model):
    _inherit = 'pos.config'

    url = fields.Char(string='URL')
    pos_machine_id = fields.Char(string='POSID')

class ResPartner(models.Model):
    _inherit = "res.partner"

    buyer_ntn = fields.Char(string='BuyerNTN')
    buyer_cnic = fields.Char(string='BuyerCNIC')

class PosJournal(models.Model):
    _inherit = "pos.payment.method"

    payment_mode = fields.Selection([('cash', 'Cash'),('card', 'Card'), ('gift', 'Gift Voucher'), ('loyalty', 'Loyalty Card'), ('mixed', 'Mixed'), ('cheque', 'Cheque')])

class PosOrder(models.Model):
    _inherit = 'pos.order'

    invoice_number = fields.Char(string='InvoiceNumber')
    res_message = fields.Char(string="Response Message")
    res_errors = fields.Char(string="Errors")

    def get_payment_type(self):
        payment_ids = self.mapped('payment_ids').filtered(lambda x: x.payment_method_id and x.payment_method_id.payment_mode)
        if all(line.payment_method_id.payment_mode == 'cash' for line in payment_ids):
            return 1
        if all(line.payment_method_id.payment_mode == 'card' for line in payment_ids):
            return 2
        if (line.payment_method_id.payment_mode == 'card' and line.payment_method_id.payment_mode == 'cash' for line in payment_ids):
            return 5

    def get_invoice_type(self):
        payment_ids = self.mapped('payment_ids').filtered(lambda x: x.payment_method_id and x.payment_method_id.payment_mode)
        if all(line.payment_method_id.payment_mode == 'cash' for line in payment_ids):
            return 1
        if all(line.payment_method_id.payment_mode == 'card' for line in payment_ids):
            return 2
        else:
            return 1

    @api.model
    def _prepare_pos_lines(self, order):
        data = []
        total_discount = 0.0
        for line in order.lines:
            total_discount += ((line.qty * line.price_unit) - line.price_subtotal)
            data.append({
                "ItemCode":line.product_id.default_code or '',
                "ItemName" : line.product_id.name,
                "Quantity" : line.qty,
                "PCTCode" : line.product_id.product_tmpl_id.hs_code_id and line.product_id.product_tmpl_id.hs_code_id.hs_code or '',
                "TaxRate" : line.tax_ids_after_fiscal_position and line.tax_ids_after_fiscal_position[0].name or 0.0, 
                "SaleValue" : line.price_unit or 0.0,
                "TotalAmount" :line.price_subtotal_incl or 0.0,
                "TaxCharged" : abs((line.price_subtotal_incl - line.price_subtotal)) or 0.0,
                "Discount" : abs((line.qty * line.price_unit) - line.price_subtotal) or 0.0,
                "FurtherTax" : 0.0,
                "InvoiceType" : self.get_invoice_type(),
                "RefUSIN" : 0.0,
            })
        print("DATA>>>>>>>>>>>>",data)

        return data , total_discount

    def _send_invoice_data(self, order_ids):
        orders = self.browse(order_ids)
        data = {}
        for order in orders.filtered(lambda x: x.partner_id):
            lines, total_discount = self._prepare_pos_lines(order)
            data.update({
                "InvoiceNumber" : '',
                "POSID" : order.config_id.pos_machine_id,
                "USIN" : order.pos_reference,
                "DateTime" :fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "BuyerNTN" : order.partner_id and order.partner_id.buyer_ntn or '',
                "BuyerCNIC" : order.partner_id and order.partner_id.buyer_cnic or '',
                "BuyerName" : order.partner_id and order.partner_id.name or '',
                "BuyerPhoneNumber" : order.partner_id and order.partner_id.phone or '',
                "TotalBillAmount" : order.amount_total,
                "TotalQuantity" : sum(order.lines.mapped('qty')) or 0.0,
                "TotalSaleValue" : sum(order.lines.mapped('price_subtotal')) or 0.0,
                "TotalTaxCharged" : order.amount_tax or 0.0,
                "Discount" : abs(total_discount) or 0.0,
                "FurtherTax" : 0.0,
                "PaymentMode" : order.get_payment_type(),
                "RefUSIN" : 0.0,
                "InvoiceType" : order.get_invoice_type(),
                "items" : lines,
            })
            
            print("DATA>>>>>>>>>>>>",data)
            
            
            str_inv_response = requests.post(order.config_id.url, data=json.dumps(data), headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Verkkomaksut-Api-Version': '1',}, verify=False)
            # str_inv_response = '{"InvoiceNumber":"9107392024132352695","Code":"100","Response":"Fiscal Invoice Number generated successfully.", "Errors":null}'
            
            print("STR INV>>>>>>>>>>>>>>>>>",str_inv_response.text)
            print("Type>>>>>>>>>>>>>>",type(str_inv_response.text))
            inv_response = json.loads(str_inv_response.text)

            print("INV_Response>>>>>>>>>>>>",inv_response)
            
            
            if inv_response:
                order.write({'invoice_number': inv_response.get('InvoiceNumber', ''), 'res_message' : inv_response.get('Response', ''), 'res_errors' : inv_response.get('Errors', '')})
                

        return True

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_data = super(PosOrder, self).create_from_ui(orders, draft=draft)
        order_ids = []
        for order in order_data:
            order_ids.append(order.get('id'))
        self._send_invoice_data(order_ids)
        print("ORDERDDDDDDDDDDDDDD", order_data)
        
        return order_data
