# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_credit_card_summary.card_summary_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_client_time(self, client_date):
        from datetime import datetime
        if not client_date:
            return False
        date = client_date.strftime('%Y-%m-%d %H:%M:%S')
        if date:
            user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
            local = pytz.timezone(user_tz)
            date = datetime.strftime(pytz.utc.localize(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S")
        return date

    def _get_card_data(self, start_at, stop_at, shop_ids):
        data = []
        domain = [
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59'),
            ('shop_id', 'in', shop_ids.ids),
        ]
        order_ids = self.env['pos.order'].sudo().search(domain)

        for order in order_ids:
            cash_amt = sum([payment.amount for payment in order.payment_ids.filtered(lambda x: x.payment_method_id.is_cash_count)])
            card_amt = sum([payment.amount for payment in order.payment_ids.filtered(lambda x: not x.payment_method_id.is_cash_count)])
            card_no = ', '.join([payment.cc_pin or '' for payment in order.payment_ids.filtered(lambda x: not x.payment_method_id.is_cash_count)])
            if card_amt > 0:
                data.append({
                    'shop_name': order.shop_id.name or '',
                    'settlement_date': '',
                    'merchant_id': '',
                    'date': self.get_client_time(order.create_date),
                    'invoice': order.pos_reference,
                    'card_no': card_no,
                    'cash_amt': cash_amt,
                    'card_amt': card_amt,
                    'invoice_amount': order.amount_paid,
                })
        return data

    def _get_card_total(self, data):
        total_dict = {
            'invoice_amount': 0,
            'cash_amt': 0,
            'card_amt': 0,
        }
        for val in data:
            total_dict['cash_amt'] += val['cash_amt']
            total_dict['card_amt'] += val['card_amt']
            total_dict['invoice_amount'] += val['invoice_amount']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))

        data = self._get_card_data(start_at, stop_at, shop_ids)

        sheet = workbook.add_worksheet("Credit Card Summary Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1, 'valign': 'vcenter'})
        format3 = workbook.add_format({'font_size': 10})
        format6 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '#,##0.00'})
        format7 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6})
        format1.set_align('center')
        format2.set_align('center')
        format5.set_align('center')
        format6.set_align('center')
        format7.set_align('center')

        sheet.merge_range('A1:I2', 'Credit Card Summary Report', format1)
        sheet.merge_range('A3:I3', 'From : ' + start_at + ' To ' + stop_at , format5)


        headers = ['Outlet', 'Settlement Date', 'Merchant ID', 'Date', 'Invoice', 'Card No', 'Cash', 'Card', 'Invoice Amount']
        row = 3
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 4
        col = 0
        for val in data:
            sheet.write(row, col+0, val['shop_name'], format3)
            sheet.write(row, col+1, val['settlement_date'], format3)
            sheet.write(row, col+2, val['merchant_id'], format3)
            sheet.write(row, col+3, val['date'], format6)
            sheet.write(row, col+4, val['invoice'], format6)
            sheet.write(row, col+5, val['card_no'], format3)
            sheet.write(row, col+6, val['cash_amt'], format3)
            sheet.write(row, col+7, val['card_amt'], format3)
            sheet.write(row, col+8, val['invoice_amount'], format3)
            row += 1

        # # Sheet Total
        total_dict = self._get_card_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+6, total_dict['cash_amt'], format7)
        sheet.write(row, col+7, total_dict['card_amt'], format7)
        sheet.write(row, col+8, total_dict['invoice_amount'], format7)
