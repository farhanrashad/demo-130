# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_mobile_data_report.mobile_data_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_pos_data(self, start_at, stop_at, shop_ids):
        data = []
        domain = [
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59')
        ]
        if len(shop_ids) > 0:
            domain += [('shop_id', 'in', shop_ids)]

        order_ids = self.env['pos.order'].sudo().search(domain)
        partner_ids = order_ids.mapped('partner_id')
        s_no = 1
        for partner in partner_ids.filtered(lambda x: x.mobile):
            orders = order_ids.filtered(lambda x: x.partner_id.id == partner.id)
            shop_count = len(orders.mapped('shop_id'))
            data.append({
                's_no': s_no,
                'mobile': partner.mobile or '',
                'name': partner.name,
                'email': partner.email or '',
                'shop_count': int(shop_count),
                'order_count': len(orders),
                'total': sum(orders.mapped('amount_total')),
            })
            s_no += 1
        return data

    def _get_pos_total(self, data):
        total_dict = {'shop_count': 0, 'order_count': 0, 'total': 0}
        for val in data:
            total_dict['shop_count'] += val['shop_count']
            total_dict['order_count'] += val['order_count']
            total_dict['total'] += val['total']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = data.get('shop_ids')

        data = self._get_pos_data(start_at, stop_at, shop_ids)

        sheet = workbook.add_worksheet("Mobile Data Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format3 = workbook.add_format({'font_size': 10})
        format6 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '#,##0.00'})
        format7 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6})
        format1.set_align('center')
        format5.set_align('center')
        format6.set_align('center')
        format7.set_align('center')

        sheet.merge_range('A1:G2', 'Mobile Data Report', format1)
        sheet.merge_range('A3:G3', 'From : ' + start_at + ' To ' + stop_at , format5)
        path = ''
        headers = ['S.No.', 'Cell No.', 'Full Name', 'Email', 'Shops Visited', 'No. Of Invoices', 'Total Purchasing']
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 6
        col = 0
        for val in data:
            sheet.write(row, col+0, val['s_no'], format6)
            sheet.write(row, col+1, val['mobile'], format3)
            sheet.write(row, col+2, val['name'], format3)
            sheet.write(row, col+3, val['email'], format3)
            sheet.write(row, col+4, val['shop_count'], format6)
            sheet.write(row, col+5, val['order_count'], format6)
            sheet.write(row, col+6, val['total'], format3)
            row += 1

        # Sheet Total
        total_dict = self._get_pos_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+4, total_dict['shop_count'], format7)
        sheet.write(row, col+5, total_dict['order_count'], format7)
        sheet.write(row, col+6, total_dict['total'], format4)
