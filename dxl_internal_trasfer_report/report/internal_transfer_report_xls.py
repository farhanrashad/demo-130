# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_internal_trasfer_report.int_trans_xlsx'
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

    def _get_stock_data(self, start_at, stop_at, location_id, location_dest_id, state, category_ids):
        data = []
        domain = [
            ('picking_type_id.code', '=', 'internal'),
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59'),]
        if location_id and location_dest_id:
            domain += ['&', ('location_id', '=', location_id.id), ('location_dest_id', '=', location_dest_id.id)]
        if location_id and not location_dest_id:
            domain += [('location_id', '=', location_id.id)]
        if location_dest_id and not location_id:
            domain += [('location_dest_id', '=', location_dest_id.id)]
        if state:
            domain += [('state', 'in', state)]
        picking_ids = self.env['stock.picking'].sudo().search(domain)
        moves = picking_ids.mapped('move_lines')
        if len(category_ids) > 0:
            moves = moves.filtered(lambda x: x.product_id.categ_id.id in category_ids)

        for move in moves:
            size = ', '.join(move.product_id.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Size').mapped('name'))
            tax = sum(move.product_id.taxes_id.mapped('amount'))
            product_price = ((move.product_id.list_price * tax) / 100) + move.product_id.list_price
            data.append({
                'picking_name': move.picking_id.name,
                'create_date': self.get_client_time(move.create_date),
                'barcode': move.product_id.barcode or '',
                'categ_name': move.product_id.categ_id.name,
                'product_name': move.product_id.name,
                'size': size or '',
                'default_code': move.product_id.default_code,
                'qty': move.quantity_done if move.state == 'done' else move.product_uom_qty,
                'state': move.state,
                'location_id': move.location_id.complete_name,
                'location_dest_id': move.location_dest_id.complete_name,
                'date_done': self.get_client_time(move.picking_id.date_done),
                'unit_price': product_price,
                'price': product_price * (move.quantity_done if move.state == 'done' else move.product_uom_qty),
                'note': move.picking_id.reference or '',
            })
        return data

    def _get_stock_total(self, data):
        total_dict = {'qty': 0, 'unit_price': 0, 'price': 0}
        for val in data:
            total_dict['qty'] += val['qty']
            total_dict['unit_price'] += val['unit_price']
            total_dict['price'] += val['price']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        location_id = self.env['stock.location'].sudo().browse(data.get('location_id'))
        location_dest_id = self.env['stock.location'].sudo().browse(data.get('location_dest_id'))
        state = data.get('state')
        category_ids = data.get('category_ids')
        data = self._get_stock_data(start_at, stop_at, location_id, location_dest_id, state, category_ids)

        sheet = workbook.add_worksheet("Stock Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '0.00'})
        # format1.set_align('center')

        sheet.merge_range('A1:D2', 'Internal Transfer Report', format1)
        sheet.merge_range('A3:D3', 'From : ' + start_at + ' To ' + stop_at , format5)
        path = ''
        if location_id:
            path += 'From : ' + location_id.complete_name
        if location_dest_id:
            path += ' To ' + location_dest_id.complete_name
        sheet.merge_range('A4:D4', path , format5)
        headers = ["Transfer Order Number", "Create Date", "Barcode", "Product Category", "Internal Reference", "Product Name", "Size", "Quantity", "Status", "From Location", "To Location", "Received Date", "Unit Retail price with tax", "Retail price with tax", "Remark"]
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 6
        col = 0
        for val in data:
            sheet.write(row, col+0, val['picking_name'], format3)
            sheet.write(row, col+1, val['create_date'], format3)
            sheet.write(row, col+2, val['barcode'], format3)
            sheet.write(row, col+3, val['categ_name'], format3)
            sheet.write(row, col+4, val['default_code'], format3)
            sheet.write(row, col+5, val['product_name'], format3)
            sheet.write(row, col+6, val['size'], format3)
            sheet.write(row, col+7, val['qty'], num_format)
            sheet.write(row, col+8, val['state'], num_format)
            sheet.write(row, col+9, val['location_id'], num_format)
            sheet.write(row, col+10, val['location_dest_id'], num_format)
            sheet.write(row, col+11, val['date_done'], num_format)
            sheet.write(row, col+12, val['unit_price'], num_format)
            sheet.write(row, col+13, val['price'], num_format)
            sheet.write(row, col+14, val['note'], num_format)
            row += 1

        # Sheet Total
        total_dict = self._get_stock_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+7, total_dict['qty'], format4)
        sheet.write(row, col+12, total_dict['unit_price'], format4)
        sheet.write(row, col+13, total_dict['price'], format4)
