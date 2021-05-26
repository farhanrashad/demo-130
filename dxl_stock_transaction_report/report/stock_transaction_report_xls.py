# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_stock_transaction_report.stock_trans_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_onhand(self, warehouse_id, category_ids):
        quants = self.env['stock.quant'].search([
            ('location_id.usage', '=', 'internal'),
            ('location_id.wh_id', '=', warehouse_id),
            ('product_id.categ_id', 'in', category_ids.ids)])
        categ_stock = {}
        for categ_id in category_ids:
            categ_stock[categ_id.id] = sum(quants.filtered(lambda x: x.product_id.categ_id.id == categ_id.id).mapped('quantity'))
        return categ_stock

    def _get_sale_data(self, start_at, stop_at, warehouse_id):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('picking_type_id.code', '=', 'outgoing'),
            ('location_id.usage', '=', 'internal'),
            ('location_dest_id.usage', '=', 'customer'),
            ('location_id.wh_id', '=', warehouse_id),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].sudo().search(domain)

    def _get_sale_return_data(self, start_at, stop_at, warehouse_id):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('picking_type_id.code', '!=', 'internal'),
            ('location_id.usage', '=', 'customer'),
            ('location_dest_id.usage', '=', 'internal'),
            ('location_dest_id.wh_id', '=', warehouse_id),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].sudo().search(domain)

    def _get_stock_purchase_data(self, start_at, stop_at, warehouse_id):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('picking_type_id.code', '=', 'incoming'),
            ('location_id.usage', '=', 'supplier'),
            ('location_dest_id.usage', '=', 'internal'),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].sudo().search(domain)

    def _get_stock_adj_data(self, start_at, stop_at, warehouse_id):
        query = """SELECT 
                    inventory.category_id as category_id,
                    sum(inventory.quantity) as quantity
                    from (select 
                    pc.id as category_id,
                    sum(-m.product_uom_qty) as quantity
                    from stock_move as m
                    LEFT join product_product as p on (p.id = m.product_id)
                    LEFT join product_template as pt on (pt.id = p.product_tmpl_id)
                    LEFT join product_category as pc on (pc.id = pt.categ_id)
                    LEFT JOIN stock_location ls on (ls.id=m.location_id)
                    LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
                    where ls.wh_id = %(warehouse_id)s
                    and (ls.usage = 'internal' and ld.usage = 'inventory')
                    and m.state = 'done'
                    and m.date > %(start_at)s and m.date < %(stop_at)s
                    group by  pc.id
                    UNION ALL
                    select 
                    pc.id as category_id,
                    sum(m.product_uom_qty) as quantity
                    from stock_move as m
                    LEFT join product_product as p on (p.id = m.product_id)
                    LEFT join product_template as pt on (pt.id = p.product_tmpl_id)
                    LEFT join product_category as pc on (pc.id = pt.categ_id)
                    LEFT JOIN stock_location ls on (ls.id=m.location_id)
                    LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
                    where ld.wh_id = %(warehouse_id)s
                    and (ls.usage = 'inventory' and ld.usage = 'internal')
                    and m.state = 'done'
                    and m.date > %(start_at)s and m.date < %(stop_at)s
                    group by  pc.id, m.date) as inventory
                    group by inventory.category_id"""
        self.env.cr.execute(query , {'start_at': start_at + ' 00:00:00', 'stop_at': stop_at + ' 23:59:59', 'warehouse_id': warehouse_id})
        res = self.env.cr.dictfetchall()
        return self._get_group_by_category(res)

    def _get_stock_trans_in_data(self, start_at, stop_at, warehouse_id):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('picking_id.picking_type_code', '=', 'internal'),
            ('location_dest_id.usage', '=', 'internal'),
            ('location_dest_id.wh_id', '=', warehouse_id),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].sudo().search(domain)

    def _get_stock_trans_out_data(self, start_at, stop_at, warehouse_id):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('location_id.usage', '=', 'internal'),
            ('picking_id.picking_type_code', '=', 'internal'),
            ('location_id.wh_id', '=', warehouse_id),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].sudo().search(domain)

    def _get_opening_stock(self, start_at, warehouse_id):
        query = """SELECT 
                    inventory.category_id as category_id,
                    sum(inventory.quantity) as quantity
                    from (select 
                    pc.id as category_id,
                    m.date as date,
                    sum(-m.product_uom_qty) as quantity
                    from stock_move as m
                    LEFT join product_product as p on (p.id = m.product_id)
                    LEFT join product_template as pt on (pt.id = p.product_tmpl_id)
                    LEFT join product_category as pc on (pc.id = pt.categ_id)
                    LEFT JOIN stock_location ls on (ls.id=m.location_id)
                    LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
                    where ls.wh_id = %(warehouse_id)s and (ls.usage = 'internal' and ld.usage != 'internal') and m.state = 'done'
                    group by  pc.id, m.date
                    UNION ALL
                    select 
                        pc.id as category_id,
                        m.date as date,
                        sum(m.product_uom_qty) as quantity
                    from stock_move as m
                    LEFT join product_product as p on (p.id = m.product_id)
                    LEFT join product_template as pt on (pt.id = p.product_tmpl_id)
                    LEFT join product_category as pc on (pc.id = pt.categ_id)
                    LEFT JOIN stock_location ls on (ls.id=m.location_id)
                    LEFT JOIN stock_location ld on (ld.id=m.location_dest_id)
                    where ld.wh_id = %(warehouse_id)s and (ls.usage != 'internal' and ld.usage = 'internal') and m.state = 'done'
                    group by  pc.id, m.date) as inventory
                    where inventory.date < %(start_at)s
                    group by inventory.category_id"""
        self.env.cr.execute(query , {'start_at': start_at + ' 00:00:00', 'warehouse_id': warehouse_id})
        return self.env.cr.dictfetchall()

    def _get_group_by_category(self, stock_data):
        category_data = {}
        for line in stock_data:
            categ_id = line.get('category_id')
            category_data[categ_id] = line.get('quantity')
        return category_data

    def _get_stock_data(self, start_at, stop_at, shop):
        data = []
        warehouse_id = shop.warehouse_id.id
        shop_data = self._get_opening_stock(start_at, warehouse_id)
        category_ids = self.env['product.category'].search([('visible_in_reporting', '=', True)])
        category_data = self._get_group_by_category(shop_data)
        stock_in_data = self._get_stock_trans_in_data(start_at, stop_at, warehouse_id)
        stock_out_data = self._get_stock_trans_out_data(start_at, stop_at, warehouse_id)
        sale_data = self._get_sale_data(start_at, stop_at, warehouse_id)
        sale_return_data = self._get_sale_return_data(start_at, stop_at, warehouse_id)
        purchase_data = self._get_stock_purchase_data(start_at, stop_at, warehouse_id)
        stock_adj_data = self._get_stock_adj_data(start_at, stop_at, warehouse_id)
        onhand_data = self._get_onhand(warehouse_id, category_ids)
        for category in category_ids:
            open_qty = category_data.get(category.id) or 0.0
            in_qty = sum(stock_in_data.filtered(lambda x: x.product_id.categ_id.id == category.id).mapped('product_uom_qty'))
            out_qty = sum(stock_out_data.filtered(lambda x: x.product_id.categ_id.id == category.id).mapped('product_uom_qty'))
            sale_qty = sum(sale_data.filtered(lambda x: x.product_id.categ_id.id == category.id).mapped('quantity_done'))
            purchase_qty = sum(purchase_data.filtered(lambda x: x.product_id.categ_id.id == category.id).mapped('quantity_done'))
            sale_return_qty = sum(sale_return_data.filtered(lambda x: x.product_id.categ_id.id == category.id).mapped('product_uom_qty'))
            adj_qty = stock_adj_data.get(category.id) or 0.0
            # on_hand = open_qty + in_qty - out_qty - sale_qty + sale_return_qty + purchase_qty + adj_qty
            data.append({
                'categ_name': category.name,
                'open_qty': open_qty,
                'purchase_qty': purchase_qty,
                'in_qty': in_qty,
                'out_qty': out_qty,
                'adj_qty': adj_qty,
                'sale_qty': sale_qty,
                'sale_return_qty': sale_return_qty,
                'on_hand': onhand_data.get(category.id) or 0
            })
        return data

    def _get_stock_total(self, data):
        total_dict = {'open_qty': 0, 'purchase_qty': 0, 'in_qty': 0, 'out_qty': 0, 'adj_qty': 0, 'sale_qty': 0, 'sale_return_qty': 0, 'on_hand': 0}
        for val in data:
            total_dict['open_qty'] += val['open_qty']
            total_dict['purchase_qty'] += val['purchase_qty']
            total_dict['in_qty'] += val['in_qty']
            total_dict['out_qty'] += val['out_qty']
            total_dict['adj_qty'] += val['adj_qty']
            total_dict['sale_qty'] += val['sale_qty']
            total_dict['sale_return_qty'] += val['sale_return_qty']
            total_dict['on_hand'] += val['on_hand']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))

        sheet = workbook.add_worksheet("Stock Transaction Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        format6 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3'})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6})
        format1.set_align('center')
        format5.set_align('center')
        format6.set_align('center')

        sheet.merge_range('A1:I2', 'Stock Transaction Report', format1)
        sheet.merge_range('A3:I3', 'From : ' + start_at + ' To ' + stop_at , format5)

        headers = ['Product Category', 'Day Opening Qty', 'Purchase', 'Receive (Transfer In)',  'Issue (Transfer Out)', 'Adjustment', 'Sale[qty]', 'Sale Return', 'On Hand']
        row = 5
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        for shop in shop_ids:
            data = self._get_stock_data(start_at, stop_at, shop)
            sheet.merge_range(row+1, 0, row+1, 8, shop.name, format6)
            row += 2
            col = 0
            for val in data:
                sheet.write(row, col+0, val['categ_name'], format3)
                sheet.write(row, col+1, val['open_qty'], format3)
                sheet.write(row, col+2, val['purchase_qty'], format3)
                sheet.write(row, col+3, val['in_qty'], format3)
                sheet.write(row, col+4, val['out_qty'], format3)
                sheet.write(row, col+5, val['adj_qty'], format3)
                sheet.write(row, col+6, val['sale_qty'], format3)
                sheet.write(row, col+7, val['sale_return_qty'], format3)
                sheet.write(row, col+8, val['on_hand'], format3)
                row += 1

            # Sheet Total
            total_dict = self._get_stock_total(data)
            # row += 1
            sheet.write(row, col+0, 'Total', format5)
            sheet.write(row, col+1, total_dict['open_qty'], format4)
            sheet.write(row, col+2, total_dict['purchase_qty'], format4)
            sheet.write(row, col+3, total_dict['in_qty'], format4)
            sheet.write(row, col+4, total_dict['out_qty'], format4)
            sheet.write(row, col+5, total_dict['adj_qty'], format4)
            sheet.write(row, col+6, total_dict['sale_qty'], format4)
            sheet.write(row, col+7, total_dict['sale_return_qty'], format4)
            sheet.write(row, col+8, total_dict['on_hand'], format4)
