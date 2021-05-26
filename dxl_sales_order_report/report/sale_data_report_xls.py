# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_sales_order_report.sale_data_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_client_time(self, client_date):
        from datetime import datetime
        if not client_date:
            return ''
        date = client_date.strftime('%Y-%m-%d %H:%M:%S')
        if date:
            user_tz = self.env.user.tz or self.env.context.get('tz') or 'UTC'
            local = pytz.timezone(user_tz)
            date = datetime.strftime(pytz.utc.localize(datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(local),"%Y-%m-%d %H:%M:%S")
        return date

    def _prepare_stock_move_date(self, stock_moves):
        delivery_moves = {}
        return_moves = {}
        for move in stock_moves:
            if not move.origin_returned_move_id:
                delivery_moves[move.sale_line_id.id] = self.get_client_time(move.date) or ''
            else:
                return_moves[move.sale_line_id.id] = self.get_client_time(move.date) or ''
        return delivery_moves, return_moves

    def _prepare_account_move_date(self, order_line_ids):
        invoice_moves = {}
        refund_moves = {}
        for line in order_line_ids:
            out_invoice = line.order_id.invoice_ids.filtered(lambda x: x.type == 'out_invoice')
            invoice_moves[line.id] =  out_invoice and self.get_client_time(out_invoice[0].create_date) or ''
            out_refund = line.order_id.invoice_ids.filtered(lambda x: x.type == 'out_refund')
            refund_moves[line.id] = out_refund and self.get_client_time(out_refund[0].create_date) or ''
        return invoice_moves, refund_moves

    def _get_sale_data(self, start_at, stop_at):
        data = []
        domain = [
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59'),
            ('order_id.state', '=', 'sale')
        ]

        order_line_ids = self.env['sale.order.line'].sudo().search(domain)
        states = {
            'draft': 'Quotation',
            'sent': 'Quotation Sent',
            'sale': 'Sales Order',
            'done': 'Locked',
            'cancel': 'Cancelled'
        }
        stock_moves = self.env['stock.move'].search([('sale_line_id', 'in', order_line_ids.ids), ('state', '=', 'done')])
        delivery_moves, return_moves = self._prepare_stock_move_date(stock_moves)
        invoice_moves, refund_moves = self._prepare_account_move_date(order_line_ids)
        for line in order_line_ids:
            order_id = line.order_id

            # do_move = stock_moves.filtered(lambda x: x.sale_line_id.id == line.id and not x.origin_returned_move_id)
            # return_move = stock_moves.filtered(lambda x: x.sale_line_id.id == line.id and x.origin_returned_move_id)

            # invoice_line_ids = order_id.invoice_ids.mapped('invoice_line_ids').filtered(lambda x: x.move_id.type == 'out_invoice' and x.product_id.id == line.product_id.id)
            # refund_line_ids = order_id.invoice_ids.mapped('invoice_line_ids').filtered(lambda x: x.move_id.type == 'out_refund' and x.product_id.id == line.product_id.id)

            color = ', '.join(line.product_id.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Color').mapped('name'))
            size = ', '.join(line.product_id.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Size').mapped('name'))

            data.append({
                'sale_order': order_id.name,
                'barcode': line.product_id.barcode or '',
                'product': line.product_id.name or '',
                'description': line.name,
                'color': color,
                'size': size,
                'qty': int(line.product_uom_qty),
                'qty_delivered': int(line.qty_delivered),
                'qty_invoiced': int(line.qty_invoiced),
                'status': states[order_id.state],
                'retail_price': line.price_unit,
                'discount': line.discount,
                'total': line.price_subtotal,
                'customer': order_id.partner_id.name,
                'ref': order_id.client_order_ref or '',
                'create_date': self.get_client_time(order_id.date_order),
                'date_done': delivery_moves.get(line.id) or '',#do_move and self.get_client_time(do_move[0].date) or '',
                'invoice_date': invoice_moves.get(line.id) or '',#invoice_line_ids and self.get_client_time(invoice_line_ids[0].create_date) or '',
                'delivery_return_date': return_moves.get(line.id) or '',#return_move and self.get_client_time(return_move[0].date) or '',
                'credit_note_date': refund_moves.get(line.id) or '',#refund_line_ids and self.get_client_time(refund_line_ids[0].create_date) or '',
            })
        return data

    def _get_sale_total(self, data):
        total_dict = {'qty': 0, 'qty_delivered': 0, 'qty_invoiced': 0, 'retail_price': 0, 'total': 0}
        for val in data:
            total_dict['qty'] += val['qty']
            total_dict['qty_delivered'] += val['qty_delivered']
            total_dict['qty_invoiced'] += val['qty_invoiced']
            total_dict['retail_price'] += val['retail_price']
            total_dict['total'] += val['total']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')

        data = self._get_sale_data(start_at, stop_at)

        sheet = workbook.add_worksheet("Ecommerce Order Report")
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

        sheet.merge_range('A1:C2', 'Ecommerce Order Report', format1)
        sheet.merge_range('A3:C3', 'From : ' + start_at + ' To ' + stop_at , format5)
        path = ''
        headers = ['Sale Order Number', 'Barcode', 'Product', 'Description', 'Color', 'Size', 'Ordered Qty', 'Delivered Qty', 'Invoiced Qty', 'Status', 'Retail Price', 'Discount', 'Total Amount', 'Customer', 'Customer Order Reference', 'Created Date', 'Delivered Date', 'Invoice Date', 'Deliver Return Date', 'Credit Note Date']
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 6
        col = 0
        for val in data:
            sheet.write(row, col+0, val['sale_order'], format3)
            sheet.write(row, col+1, val['barcode'], format3)
            sheet.write(row, col+2, val['product'], format3)
            sheet.write(row, col+3, val['description'], format3)
            sheet.write(row, col+4, val['color'], format3)
            sheet.write(row, col+5, val['size'], format3)
            sheet.write(row, col+6, val['qty'], format3)
            sheet.write(row, col+7, val['qty_delivered'], format3)
            sheet.write(row, col+8, val['qty_invoiced'], format3)
            sheet.write(row, col+9, val['status'], format3)
            sheet.write(row, col+10, val['retail_price'], format3)
            sheet.write(row, col+11, val['discount'], format3)
            sheet.write(row, col+12, val['total'], format3)
            sheet.write(row, col+13, val['customer'], format3)
            sheet.write(row, col+14, val['ref'], format3)
            sheet.write(row, col+15, val['create_date'], format3)
            sheet.write(row, col+16, val['date_done'], format3)
            sheet.write(row, col+17, val['invoice_date'], format3)
            sheet.write(row, col+18, val['delivery_return_date'], format3)
            sheet.write(row, col+19, val['credit_note_date'], format3)
            row += 1

        # Sheet Total
        total_dict = self._get_sale_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+6, total_dict['qty'], format7)
        sheet.write(row, col+7, total_dict['qty_delivered'], format7)
        sheet.write(row, col+8, total_dict['qty_invoiced'], format7)
        sheet.write(row, col+10, total_dict['retail_price'], format4)
        sheet.write(row, col+12, total_dict['total'], format4)
