# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_fbr_invoice_report.fbr_invoice_xlsx'
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

    def _get_pos_data(self, start_at, stop_at, shop_ids):
        data = []
        domain = [
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59'),
            ('shop_id', 'in', shop_ids.ids),
        ]
        order_ids = self.env['pos.order'].sudo().search(domain)

        for order in order_ids:
            discount = sum([(line.price_unit * line.qty) - line.price_subtotal for line in order.lines])
            cash_sale = sum(order.payment_ids.filtered(lambda x: x.payment_method_id.is_cash_count == True).mapped('amount'))
            card_sale = sum(order.payment_ids.filtered(lambda x: x.payment_method_id.is_cash_count == False).mapped('amount'))
            data.append({
                'shop_name': order.shop_id and order.shop_id.name or '',
                'fbr_pos_id': order.session_id.config_id.pos_machine_id or '',
                'date': self.get_client_time(order.create_date),
                'receipt_number': order.pos_reference,
                'invoice_number': order.invoice_number or '',
                'cash_sale': cash_sale,
                'card_sale': card_sale,
                'sale_return': 0.0,
                'discount': discount,
                'net_amount': order.amount_total,
            })
        return data

    def _get_pos_total(self, data):
        total_dict = {
            'cash_sale': 0,
            'card_sale': 0,
            'discount': 0,
            'net_amount': 0
        }
        for val in data:
            total_dict['cash_sale'] += val['cash_sale']
            total_dict['card_sale'] += val['card_sale']
            total_dict['discount'] += val['discount']
            total_dict['net_amount'] += val['net_amount']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))

        data = self._get_pos_data(start_at, stop_at, shop_ids)

        sheet = workbook.add_worksheet("FBR Invoice Report")
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

        sheet.merge_range('A1:J2', 'FBR Invoice Report', format1)
        sheet.merge_range('A3:J3', 'From : ' + start_at + ' To ' + stop_at , format5)


        headers = ['Outlet', 'POS Reg #', 'Date', 'Odoo Invoice #', 'FBR Inv #', 'Cash Sale', 'Card Sale', 'Sale Return', 'Discount', 'Net Amount']
        
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
            sheet.write(row, col+1, val['fbr_pos_id'], format3)
            sheet.write(row, col+2, val['date'], format3)
            sheet.write(row, col+3, val['receipt_number'], format6)
            sheet.write(row, col+4, val['invoice_number'], format6)
            sheet.write(row, col+5, val['cash_sale'], format3)
            sheet.write(row, col+6, val['card_sale'], format3)
            sheet.write(row, col+7, val['sale_return'], format3)
            sheet.write(row, col+8, val['discount'], format3)
            sheet.write(row, col+9, val['net_amount'], format3)
            row += 1

        # # Sheet Total
        total_dict = self._get_pos_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+5, total_dict['cash_sale'], format7)
        sheet.write(row, col+6, total_dict['card_sale'], format7)
        sheet.write(row, col+8, total_dict['discount'], format7)
        sheet.write(row, col+9, total_dict['net_amount'], format7)
