# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime



class ProductXlsx(models.AbstractModel):
    _name = 'report.pos_summary_report.pos_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_pos_data(self, start_at, stop_at, shop_ids):
        data = []
        domain = [('start_at', '>=', start_at + ' 00:00:00'), ('stop_at', '<=', stop_at + ' 23:59:59')]
        if len(shop_ids):
            domain.append(('config_id.shop_id', 'in', shop_ids))
        if not self.env.user.has_group('point_of_sale.group_pos_manager'):
            domain.append(('config_id', 'in', self.env.user.pos_configs.ids))
        sessions = self.env['pos.session'].search(domain)

        bank_method_ids = self.env['pos.payment.method'].search([('is_cash_count', '=', False)])
        cash_method_ids = self.env['pos.payment.method'].search([('is_cash_count', '=', True)]) 
        cash_ids = self.env['pos.cash.in.out'].search([])
        for session in sessions:
            bank_payments = session.order_ids.mapped('payment_ids').filtered(lambda x: x.payment_method_id in bank_method_ids)
            cash_payments = session.order_ids.mapped('payment_ids').filtered(lambda x: x.payment_method_id in cash_method_ids)
            opening_cash = session.cash_register_balance_start
            cash_sale = sum(cash_payments.mapped('amount'))
            card_sale = sum(bank_payments.mapped('amount'))
            available_cash = opening_cash + cash_sale
            cash_in = sum(cash_ids.filtered(lambda x: x.session_id == session and x.cash_type == 'credit').mapped('amount'))
            cash_out = sum(cash_ids.filtered(lambda x: x.session_id == session and x.cash_type == 'debit').mapped('amount'))
            closing_cash = (opening_cash + cash_sale) + cash_in - cash_out
            data.append({
                'name': session.config_id.shop_id and session.config_id.shop_id.name or session.config_id.name,
                'session': session.name,
                'start_at': session.start_at.strftime("%Y-%m-%d %H:%M:%S"),
                'stop_at': session.stop_at.strftime("%Y-%m-%d %H:%M:%S"),
                'opening_cash': opening_cash,
                'cash_sale': cash_sale,
                'card_sale': card_sale,
                'coupon': 0,
                'total_sale': cash_sale + card_sale,
                'available_cash': available_cash,
                'cash_in': cash_in,
                'cash_out': cash_out,
                'closing_cash': closing_cash,
            })
        return data

    def _get_pos_total(self, data):
        total_dict = {'opening_cash': 0, 'cash_sale': 0, 'card_sale': 0, 'coupon': 0, 'total_sale': 0, 'available_cash': 0, 'cash_in': 0, 'cash_out': 0, 'closing_cash': 0}
        for val in data:
            total_dict['opening_cash'] += val['opening_cash']
            total_dict['cash_sale'] += val['cash_sale']
            total_dict['card_sale'] += val['card_sale']
            total_dict['coupon'] += val['coupon']
            total_dict['total_sale'] += val['total_sale']
            total_dict['available_cash'] += val['available_cash']
            total_dict['cash_in'] += val['cash_in']
            total_dict['cash_out'] += val['cash_out']
            total_dict['closing_cash'] += val['closing_cash']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = data.get('shop_ids')
        print('>>>>>>>>>.', shop_ids)
        data = self._get_pos_data(start_at, stop_at, shop_ids)

        sheet = workbook.add_worksheet("Stock Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6})
        format1.set_align('center')

        sheet.merge_range('A1:M2', 'POS Summary Report', format1)
        headers = ["Shop/Location Name", "Session #", "Opening Date", "Closing Date", 'Opening Cash', 'Cash Sale', 'Cr.Card Sale', 'Gift Coupons', 'Total Sale', 'Available Cash', 'Cash In', 'Cash Out', 'Closing Cash']
        row = 2
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 3
        col = 0
        for val in data:
            sheet.write(row, col+0, val['name'], format3)
            sheet.write(row, col+1, val['session'], format3)
            sheet.write(row, col+2, val['start_at'], format3)
            sheet.write(row, col+3, val['stop_at'], format3)
            sheet.write(row, col+4, val['opening_cash'], format3)
            sheet.write(row, col+5, val['cash_sale'], format3)
            sheet.write(row, col+6, val['card_sale'], format3)
            sheet.write(row, col+7, val['coupon'], format3)
            sheet.write(row, col+8, val['total_sale'], format3)
            sheet.write(row, col+9, val['available_cash'], format3)
            sheet.write(row, col+10, val['cash_in'], format3)
            sheet.write(row, col+11, val['cash_out'], format3)
            sheet.write(row, col+12, val['closing_cash'], format3)
            row += 1

        # Sheet Total
        total_dict = self._get_pos_total(data)
        row += 1
        sheet.write(row, col+1, 'Total', format3)
        sheet.write(row, col+4, total_dict['opening_cash'], format4)
        sheet.write(row, col+5, total_dict['cash_sale'], format4)
        sheet.write(row, col+6, total_dict['card_sale'], format4)
        sheet.write(row, col+7, total_dict['coupon'], format4)
        sheet.write(row, col+8, total_dict['total_sale'], format4)
        sheet.write(row, col+9, total_dict['available_cash'], format4)
        sheet.write(row, col+10, total_dict['cash_in'], format4)
        sheet.write(row, col+11, total_dict['cash_out'], format4)
        sheet.write(row, col+12, total_dict['closing_cash'], format4)
