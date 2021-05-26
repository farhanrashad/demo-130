# -*- coding: utf-8 -*-
from odoo import models
import io
import base64
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class ProductXlsx(models.AbstractModel):
    _name = 'report.shop_wise_profit.pos_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def get_client_time(self, client_date):
        from datetime import datetime
        date = datetime.strptime(client_date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        if date:
            user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
            local = pytz.timezone(user_tz)
            date = datetime.strftime(pytz.utc.localize(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S")
        return date

    def _get_gross_sale(self, analytic_account_id, date_start, date_end):
        balance = 0.0
        pos_orders = self.env['pos.order'].sudo().search([
            ('account_analytic_id', '=', analytic_account_id.id),
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end),
        ])
        for line in pos_orders.mapped('lines'):
            balance += line.qty * line.price_unit
        return balance

    def _get_discount(self, analytic_account_id, date_start, date_end):
        balance = 0.0
        pos_orders = self.env['pos.order'].sudo().search([
            ('account_analytic_id', '=', analytic_account_id.id),
            ('date_order', '>=', self.get_client_time(date_start)),
            ('date_order', '<=', self.get_client_time(date_end)),
        ])
        for line in pos_orders.mapped('lines'):
            balance += ((line.qty * line.price_unit) - line.price_subtotal)
        return balance

    def _get_balance(self, analytic_account_id, date_start, date_end, analytic_type):
        balance = 0.0
        account_ids = self.env['account.account'].search([('analytic_type', '=', analytic_type)])
        moves = self.env['account.move.line'].sudo().search([
            ('analytic_account_id', '=', analytic_account_id.id),
            ('account_id', 'in', account_ids.ids),
            ('parent_state', '!=', 'cancel'),
            ('date', '>=', self.get_client_time(date_start)),
            ('date', '<=', self.get_client_time(date_end)),
        ])
        print('MOVE::::::::', moves.mapped('move_id'))
        balance = sum(moves.mapped('credit')) - sum(moves.mapped('debit'))
        return balance

    def _get_pos_data(self, start_at, stop_at, region_ids, analytic_acccount_ids):
        data = []
        s_no = 1
        for account in analytic_acccount_ids:
            # gross_sale = self._get_gross_sale(account, start_at, stop_at)
            gross_sale = self._get_balance(account, start_at, stop_at, 'gross_sale')
            discount = 0.00 #self._get_discount(account, start_at, stop_at)
            net_sale = gross_sale - discount
            cogs = self._get_balance(account, start_at, stop_at, 'cogs')
            admin_expense = self._get_balance(account, start_at, stop_at, 'admin_expense')
            selling_expense = self._get_balance(account, start_at, stop_at, 'selling_expense')
            financila_expense = self._get_balance(account, start_at, stop_at, 'financila_expense')
            wh_allocation = self._get_balance(account, start_at, stop_at, 'wh_allocation')
            ho_allocation = self._get_balance(account, start_at, stop_at, 'ho_allocation')
            incentive = self._get_balance(account, start_at, stop_at, 'incentive')
            pl = net_sale - abs(cogs) - abs(admin_expense) - abs(selling_expense) - abs(financila_expense) - abs(wh_allocation) - abs(ho_allocation)
            net_pl = pl + incentive
            data.append({
                's_no': s_no,
                'region': account.region_id.name or '',
                'outlet': account.name or '',
                'gross_sale': gross_sale,
                'discount': discount,
                'net_sale': net_sale,
                'cogs': cogs,
                'admin_expense': admin_expense,
                'selling_expense': selling_expense,
                'financila_expense': financila_expense,
                'wh_allocation': wh_allocation,
                'ho_allocation': ho_allocation,
                'pl': pl,
                'incentive': incentive,
                'net_pl': net_pl,
            })
            s_no += 1
        print('GROSS SALE:::::::::', data)
        return data

    # def _get_pos_total(self, data):
    #     total_dict = {'opening_cash': 0, 'cash_sale': 0, 'card_sale': 0, 'coupon': 0, 'total_sale': 0, 'available_cash': 0, 'cash_in': 0, 'cash_out': 0, 'closing_cash': 0}
    #     for val in data:
    #         total_dict['opening_cash'] += val['opening_cash']
    #         total_dict['cash_sale'] += val['cash_sale']
    #         total_dict['card_sale'] += val['card_sale']
    #         total_dict['coupon'] += val['coupon']
    #         total_dict['total_sale'] += val['total_sale']
    #         total_dict['available_cash'] += val['available_cash']
    #         total_dict['cash_in'] += val['cash_in']
    #         total_dict['cash_out'] += val['cash_out']
    #         total_dict['closing_cash'] += val['closing_cash']
    #     return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')

        region_ids = self.env['analytic.region'].sudo().browse(data.get('region_ids'))
        region_list = ', '.join(region_ids.mapped('name'))

        analytic_acccount_ids = self.env['account.analytic.account'].sudo().browse(data.get('analytic_account_ids'))
        location_list = ', '.join(analytic_acccount_ids.mapped('name'))

        data = self._get_pos_data(start_at, stop_at, region_ids, analytic_acccount_ids)

        sheet = workbook.add_worksheet("Shop Wise Profit Report")
        format1 = workbook.add_format({'font_size': 20, 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        format3 = workbook.add_format({'font_size': 10})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6})
        format5 = workbook.add_format({'font_size': 12, 'bold': True})

        format2.set_align('center')

        sheet.merge_range('A1:C1', self.env.company.name, format1)
        sheet.set_row(0, 30) # set height of first row

        sheet.merge_range('A2:B2', 'Profit and Loss Statement', format5)


        image_width = 140.0
        image_height = 182.0
        cell_width = 28.0
        cell_height = 30.0
        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        imgdata = base64.b64decode(self.env.company.logo)
        image = io.BytesIO(imgdata)
        sheet.merge_range('N1:O3', '', format1)
        sheet.insert_image('N1', "any_name.png", {'image_data': image, 'x_scale': x_scale, 'y_scale': y_scale})

        # sheet.merge_range('J1:K1', self.env.company.name, format1)
        # buf_image=io.BytesIO(self.env.company.logo)
        # sheet.insert_image('K3',base64.b64encode(self.env.company.logo),{'image_data': buf_image})


        sheet.set_column(0, 1, 16)
        sheet.write(3, 0, 'From:', format5)
        sheet.set_column(0, 1, 16)
        sheet.write(3, 1, self.get_client_time(start_at), format3)

        sheet.set_column(0, 1, 16)
        sheet.write(4, 0, 'To:', format5)
        sheet.set_column(0, 1, 16)
        sheet.write(4, 1, self.get_client_time(stop_at), format3)

        sheet.set_column(0, 1, 16)
        sheet.write(5, 0, 'Region:', format5)
        sheet.merge_range('B6:K6', region_list, format3)

        sheet.set_column(0, 1, 16)
        sheet.write(6, 0, 'Outlet:', format5)
        sheet.merge_range('B7:K7', location_list, format3)


        headers = ["S.no", "Region", "Outlet", "Gross Sale", "Discount", "Net Sales", "COGS", "Admin Expenses", "Selling Expenses", "Financial Expenses", "WH Allocation", "HO Allocation", "P/L", "Incentive Sales", "Net P/L"]
        row = 9
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 16)
            sheet.write(row, col, header, format2)
            col += 1
        sheet.set_row(row, 20)

        row = 10
        col = 0
        for val in data:
            sheet.write(row, col+0, val['s_no'], format3)
            sheet.write(row, col+1, val['region'], format3)
            sheet.write(row, col+2, val['outlet'], format3)
            sheet.write(row, col+3, val['gross_sale'], format3)
            sheet.write(row, col+4, val['discount'], format3)
            sheet.write(row, col+5, val['net_sale'], format3)
            sheet.write(row, col+6, val['cogs'], format3)
            sheet.write(row, col+7, val['admin_expense'], format3)
            sheet.write(row, col+8, val['selling_expense'], format3)
            sheet.write(row, col+9, val['financila_expense'], format3)
            sheet.write(row, col+10, val['wh_allocation'], format3)
            sheet.write(row, col+11, val['ho_allocation'], format3)
            sheet.write(row, col+12, val['pl'], format3)
            sheet.write(row, col+13, val['incentive'], format3)
            sheet.write(row, col+14, val['net_pl'], format3)
            row += 1

        # # Sheet Total
        # total_dict = self._get_pos_total(data)
        # row += 1
        # sheet.write(row, col+1, 'Total', format3)
        # sheet.write(row, col+4, total_dict['opening_cash'], format4)
        # sheet.write(row, col+5, total_dict['cash_sale'], format4)
        # sheet.write(row, col+6, total_dict['card_sale'], format4)
        # sheet.write(row, col+7, total_dict['coupon'], format4)
        # sheet.write(row, col+8, total_dict['total_sale'], format4)
        # sheet.write(row, col+9, total_dict['available_cash'], format4)
        # sheet.write(row, col+10, total_dict['cash_in'], format4)
        # sheet.write(row, col+11, total_dict['cash_out'], format4)
        # sheet.write(row, col+12, total_dict['closing_cash'], format4)
