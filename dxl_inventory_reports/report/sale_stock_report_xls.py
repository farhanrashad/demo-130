# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_inventory_reports.inv_sale_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_product_quants(self, product_ids, location_id):
        quants = self.env['stock.quant'].search([
            '|', ('location_id', 'child_of', location_id.id),
            ('location_id', '=', location_id.id),
            ('product_id', 'in', product_ids.ids)
        ])
        return quants

    def _get_promo_discount(self, product_ids, shop_id):
        product_by_discount = {}
        config_id = self.env['pos.config'].search([('shop_id', '=', shop_id)])
        promotion_ids = self.env['pos.promotion'].search([('pos_ids', 'in', config_id.id), ('state', '=', 'active')])
        promo_line_ids = promotion_ids.mapped('promotion_product_ids').filtered(lambda x: x.product_id.id in product_ids.ids)
        for line in promo_line_ids:
            if line.product_id.id in product_by_discount:
                product_by_discount[line.product_id.id] += line.disc_percentage
            else:
                product_by_discount[line.product_id.id] = line.disc_percentage
        return product_by_discount

    def _get_sale_data(self, start_at, stop_at, shop_id, category_ids, product_ids, lines):
        data = []
        stock_location_id = self.env['stock.location'].search([('usage', '=', 'internal'), ('shop_id', '=', shop_id)])
        transit_location_id = self.env['stock.location'].search([('usage', '=', 'transit'), ('shop_id', '=', shop_id)])
        transit_quants = self._get_product_quants(product_ids, transit_location_id)
        onhand_quants = self._get_product_quants(product_ids, stock_location_id)
        product_discount = self._get_promo_discount(product_ids, shop_id)
        sale_data = {}
        sale_amount_data = {}
        purchase_amount_data = {}

        stock_move_ids = self.env['stock.move'].search([('sale_line_id', 'in', lines.ids)])
        valuation_ids = self.env['stock.valuation.layer'].search([('stock_move_id', 'in', stock_move_ids.ids)])

        for p in product_ids:
            if p.id in sale_data:
                sale_data[p.id] += sum(lines.filtered(lambda x: x.product_id.id == p.id).mapped('qty'))
            else:
                sale_data[p.id] = sum(lines.filtered(lambda x: x.product_id.id == p.id).mapped('qty'))
            if p.id in sale_amount_data:
                sale_amount_data[p.id] += sum(lines.filtered(lambda x: x.product_id.id == p.id).mapped('price_subtotal_incl'))
            else:
                sale_amount_data[p.id] = sum(lines.filtered(lambda x: x.product_id.id == p.id).mapped('price_subtotal_incl'))
            if p.id in purchase_amount_data:
                purchase_amount_data[p.id] += sum(valuation_ids.filtered(lambda x: x.product_id.id == p.id).mapped('value'))
            else:
                purchase_amount_data[p.id] = sum(valuation_ids.filtered(lambda x: x.product_id.id == p.id).mapped('value'))

        for product_id in product_ids:
            lines = lines.filtered(lambda x: x.product_id.id == product_id.id)
            transit_qty = sum(transit_quants.filtered(lambda x: x.product_id.id == product_id.id).mapped('quantity'))
            on_hand_qty = sum(onhand_quants.filtered(lambda x: x.product_id.id == product_id.id).mapped('quantity'))
            color = ''
            size = ''
            for pav_id in product_id.product_template_attribute_value_ids:
                if pav_id.attribute_id.name == 'Color':
                    color = pav_id.name
                if pav_id.attribute_id.name == 'Size':
                    size = pav_id.name

            tax = sum(product_id.taxes_id.mapped('amount'))
            retail_price = ((product_id.list_price * tax) / 100) + product_id.list_price
            if on_hand_qty == 0 and transit_qty == 0 and sale_data[product_id.id] == 0:
                continue
            data.append({
                'barcode': product_id.barcode or '',
                'categ_name': product_id.categ_id.name,
                'design': product_id.default_code or '',
                'product_name': product_id.name,
                'color': color,
                'size': size,
                'on_hand_qty': on_hand_qty,
                'transit_qty': transit_qty,
                'sale_qty': sale_data[product_id.id],
                'sale_amount': sale_amount_data[product_id.id],
                'retail_price': retail_price,
                'cost': product_id.standard_price,
                'purchase_amount': purchase_amount_data[product_id.id],
                'discount': product_discount.get(product_id.id, 0),
            })
        return data

    def _get_sale_total(self, data):
        total_dict = {'on_hand_qty': 0, 'transit_qty': 0, 'sale_qty': 0, 'sale_amount': 0, 'retail_price': 0, 'cost': 0, 'purchase_amount': 0}
        for val in data:
            total_dict['on_hand_qty'] += val['on_hand_qty']
            total_dict['transit_qty'] += val['transit_qty']
            total_dict['sale_qty'] += val['sale_qty']
            total_dict['sale_amount'] += val['sale_amount']
            total_dict['retail_price'] += val['retail_price']
            total_dict['cost'] += val['cost']
            total_dict['purchase_amount'] += val['purchase_amount']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))
        category_ids = data.get('category_ids')
        product_ids = self.env['product.product'].browse(data.get('product_ids'))

        sheet = workbook.add_worksheet("Sale Vs Inventory Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        format6 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '0.00'})
        format1.set_align('center')
        format6.set_align('center')

        sheet.merge_range('A1:N2', 'Sale Vs Inventory Report', format1)
        headers = ["Barcode", "Product Category", "Internal Reference", "Product Name", "Color", 'Size', 'On Hand Qty', 'In Transit Quantity', 'Sale Quantity', 'Sale Amount', 'Retail Price', 'Cost', 'Purchase Amount', 'Current Discount(%)']
        row = 2
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        if category_ids and not product_ids:
            product_ids = self.env['product.product'].search([('categ_id', 'in', category_ids)])
        if not category_ids and not product_ids:
            product_ids = self.env['product.product'].sudo().search([])

        domain = [(('order_id.shop_id', 'in', shop_ids.ids)), ('order_id.date_order', '>=', start_at + ' 00:00:00'), ('order_id.date_order', '<=', stop_at + ' 23:59:59')]
        pos_lines = self.env['pos.order.line'].search(domain)
        for shop in shop_ids:
            lines = pos_lines.filtered(lambda x: x.order_id.shop_id.id == shop.id)
            data = self._get_sale_data(start_at, stop_at, shop.id, category_ids, product_ids, lines)
            sheet.merge_range(row+1, 0, row+1, 13, shop.name, format6)
            row += 2
            col = 0
            for val in data:
                sheet.write(row, col+0, val['barcode'], format3)
                sheet.write(row, col+1, val['categ_name'], format3)
                sheet.write(row, col+2, val['design'], format3)
                sheet.write(row, col+3, val['product_name'], format3)
                sheet.write(row, col+4, val['color'], format3)
                sheet.write(row, col+5, val['size'], num_format)
                sheet.write(row, col+6, val['on_hand_qty'], num_format)
                sheet.write(row, col+7, val['transit_qty'], num_format)
                sheet.write(row, col+8, val['sale_qty'], num_format)
                sheet.write(row, col+9, val['sale_amount'], num_format)
                sheet.write(row, col+10, val['retail_price'], num_format)
                sheet.write(row, col+11, val['cost'], num_format)
                sheet.write(row, col+12, val['purchase_amount'], num_format)
                sheet.write(row, col+13, val['discount'], num_format)
                row += 1

            # Sheet Total
            total_dict = self._get_sale_total(data)
            row += 1
            sheet.write(row, col+4, 'Total', format5)
            sheet.write(row, col+6, total_dict['on_hand_qty'], format4)
            sheet.write(row, col+7, total_dict['transit_qty'], format4)
            sheet.write(row, col+8, total_dict['sale_qty'], format4)
            sheet.write(row, col+9, total_dict['sale_amount'], format4)
            sheet.write(row, col+10, total_dict['retail_price'], format4)
            sheet.write(row, col+11, total_dict['cost'], format4)
            sheet.write(row, col+12, total_dict['purchase_amount'], format4)
