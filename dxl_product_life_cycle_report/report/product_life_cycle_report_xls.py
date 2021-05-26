# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz


class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_product_life_cycle_report.product_life_cycle_xlsx'
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

    def _get_product_qty(self, product_id, type):
        quants = self.env['stock.quant'].search([('location_id.usage', '=', type), ('product_id', '=', product_id.id)])
        return sum(quants.mapped('quantity'))

    def _get_sale(self, start_at, stop_at, product_ids):
        query = """ SELECT
            pol.product_id as product_id,
            CASE WHEN pol.discount = 0 THEN sum(pol.product_uom_qty) else 0.0 END as qty_zero,
            CASE WHEN pol.discount = 0 THEN sum(pol.price_total) else 0.0 END as sale_zero,
            CASE WHEN pol.discount > 0 and pol.discount <= 10 THEN sum(pol.product_uom_qty) else 0.0 END as qty_ten,
            CASE WHEN pol.discount > 0 and pol.discount <= 10 THEN sum(pol.price_total) else 0.0 END as sale_ten,
            CASE WHEN pol.discount > 10 and pol.discount <= 20 THEN sum(pol.product_uom_qty) else 0.0 END as qty_twenty,
            CASE WHEN pol.discount > 10 and pol.discount <= 20 THEN sum(pol.price_total) else 0.0 END as sale_twenty,
            CASE WHEN pol.discount > 20 and pol.discount <= 30 THEN sum(pol.product_uom_qty) else 0.0 END as qty_thirty,
            CASE WHEN pol.discount > 20 and pol.discount <= 30 THEN sum(pol.price_total) else 0.0 END as sale_thirty,
            CASE WHEN pol.discount > 30 and pol.discount <= 40 THEN sum(pol.product_uom_qty) else 0.0 END as qty_fourty,
            CASE WHEN pol.discount > 30 and pol.discount <= 40 THEN sum(pol.price_total) else 0.0 END as sale_fourty,
            CASE WHEN pol.discount > 40 and pol.discount <= 50 THEN sum(pol.product_uom_qty) else 0.0 END as qty_fifty,
            CASE WHEN pol.discount > 40 and pol.discount <= 50 THEN sum(pol.price_total) else 0.0 END as sale_fifty,
            CASE WHEN pol.discount > 50 and pol.discount <= 60 THEN sum(pol.product_uom_qty) else 0.0 END as qty_sixty,
            CASE WHEN pol.discount > 50 and pol.discount <= 60 THEN sum(pol.price_total) else 0.0 END as sale_sixty,
            CASE WHEN pol.discount > 60 and pol.discount <= 70 THEN sum(pol.product_uom_qty) else 0.0 END as qty_seventy,
            CASE WHEN pol.discount > 60 and pol.discount <= 70 THEN sum(pol.price_total) else 0.0 END as sale_seventy,
            CASE WHEN pol.discount > 70 THEN sum(pol.product_uom_qty) else 0.0 END as qty_seventy_up,
            CASE WHEN pol.discount > 70 THEN sum(pol.price_total) else 0.0 END as sale_seventy_up
            from sale_order_line as pol
            where pol.create_date >= %(start_at)s and pol.create_date <= %(stop_at)s and pol.product_id in %(product_ids)s
            group by pol.product_id, pol.discount
        """
        self.env.cr.execute(query , {'start_at': start_at + ' 00:00:00', 'stop_at': stop_at + ' 23:59:59', 'product_ids': tuple(product_ids.ids)})
        return self.env.cr.dictfetchall()

    def _get_pos_sale(self, start_at, stop_at, product_ids):
        query = """ SELECT
            pol.product_id as product_id,
            CASE WHEN pol.discount = 0 and COALESCE(pol.promo_disc_percentage, 0) = 0 THEN sum(pol.qty) else 0.0 END as qty_zero,
            CASE WHEN pol.discount = 0 and COALESCE(pol.promo_disc_percentage, 0) = 0 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_zero,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 0 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 10 THEN sum(pol.qty) else 0.0 END as qty_ten,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 0 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 10 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_ten,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 10 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 20 THEN sum(pol.qty) else 0.0 END as qty_twenty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 10 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 20 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_twenty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 20 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 30 THEN sum(pol.qty) else 0.0 END as qty_thirty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 20 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 30 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_thirty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 30 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 40 THEN sum(pol.qty) else 0.0 END as qty_fourty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 30 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 40 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_fourty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 40 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 50 THEN sum(pol.qty) else 0.0 END as qty_fifty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 40 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 50 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_fifty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 50 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 60 THEN sum(pol.qty) else 0.0 END as qty_sixty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 50 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 60 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_sixty,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 60 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 70 THEN sum(pol.qty) else 0.0 END as qty_seventy,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 60 and (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) <= 70 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_seventy,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 70 THEN sum(pol.qty) else 0.0 END as qty_seventy_up,
            CASE WHEN (pol.discount + COALESCE(pol.promo_disc_percentage, 0)) > 70 THEN sum(pol.price_subtotal_incl) else 0.0 END as sale_seventy_up
            from pos_order_line as pol
            where pol.create_date >= %(start_at)s and pol.create_date <= %(stop_at)s and pol.product_id in %(product_ids)s
            group by pol.product_id, pol.discount, pol.promo_disc_percentage
        """
        self.env.cr.execute(query , {'start_at': start_at + ' 00:00:00', 'stop_at': stop_at + ' 23:59:59', 'product_ids': tuple(product_ids.ids)})
        return self.env.cr.dictfetchall()

    def _get_sale_qty_value(self, product_sale_data):
        discount_limit = 0
        pd = {'0_qty': 0, '0_value': 0, '10_qty': 0, '10_value': 0, '20_qty': 0, '20_value': 0, '30_qty': 0, '30_value': 0, '40_qty': 0, '40_value': 0, '50_qty': 0, '50_value': 0, '60_qty': 0, '60_value': 0, '70_qty': 0, '70_value': 0, '70_up_qty': 0, '70_up_value': 0, 'net_sale_qty': 0, 'net_sale_value': 0}
        pd['0_qty'] = sum([line['qty_zero'] for line in product_sale_data])
        pd['0_value'] = sum([line['sale_zero'] for line in product_sale_data])
        pd['10_qty'] = sum([line['qty_ten'] for line in product_sale_data])
        pd['10_value'] = sum([line['sale_ten'] for line in product_sale_data])
        pd['20_qty'] = sum([line['qty_twenty'] for line in product_sale_data])
        pd['20_value'] = sum([line['sale_twenty'] for line in product_sale_data])
        pd['30_qty'] = sum([line['qty_thirty'] for line in product_sale_data])
        pd['30_value'] = sum([line['sale_thirty'] for line in product_sale_data])
        pd['40_qty'] = sum([line['qty_fourty'] for line in product_sale_data])
        pd['40_value'] = sum([line['sale_fourty'] for line in product_sale_data])
        pd['50_qty'] = sum([line['qty_fifty'] for line in product_sale_data])
        pd['50_value'] = sum([line['sale_fifty'] for line in product_sale_data])
        pd['60_qty'] = sum([line['qty_sixty'] for line in product_sale_data])
        pd['60_value'] = sum([line['sale_sixty'] for line in product_sale_data])
        pd['70_qty'] = sum([line['qty_seventy'] for line in product_sale_data])
        pd['70_value'] = sum([line['sale_seventy'] for line in product_sale_data])
        pd['70_up_qty'] = sum([line['qty_seventy_up'] for line in product_sale_data])
        pd['70_up_value'] = sum([line['sale_seventy_up'] for line in product_sale_data])
        pd['net_sale_qty'] = pd['0_qty'] + pd['10_qty'] + pd['20_qty'] + pd['30_qty'] + pd['40_qty'] + pd['50_qty'] + pd['60_qty'] + pd['70_qty'] + pd['70_up_qty']
        pd['net_sale_value'] = pd['0_value'] + pd['10_value'] + pd['20_value'] + pd['30_value'] + pd['40_value'] + pd['50_value'] + pd['60_value'] + pd['70_value'] + pd['70_up_value']
        return pd

    def _get_product_sale(self, sale_data, pos_data):
        product_data = {}
        for line in sale_data:
            product_id = line['product_id']
            if product_id in product_data:
                product_data[product_id].append(line)
            else:
                product_data[product_id] = [line]
        for line in pos_data:
            product_id = line['product_id']
            if product_id in product_data:
                product_data[product_id].append(line)
            else:
                product_data[product_id] = [line]
        return product_data

    def _get_purchase_data(self, start_at, stop_at, product_ids):
        domain = [
            ('date', '>=', start_at + ' 00:00:00'),
            ('date', '<=', stop_at + ' 23:59:59'),
            ('location_id.usage', '=', 'supplier'),
            ('location_dest_id.usage', '=', 'internal'),
            ('state', '=', 'done')
        ]
        return self.env['stock.move'].search(domain)

    def _get_sale_data(self, start_at, stop_at, category_ids, product_ids):
        data = []

        if category_ids and not product_ids:
            product_ids = self.env['product.product'].search([('categ_id', 'in', category_ids)])
        if not category_ids and not product_ids:
            product_ids = self.env['product.product'].sudo().search([])

        # sale_data = self._get_sale(start_at, stop_at, product_ids)
        sale_data = {}
        pos_data = self._get_pos_sale(start_at, stop_at, product_ids)
        pos_sale_data = self._get_product_sale(sale_data, pos_data)
        # product_ids = self.env['product.product'].browse(pos_sale_data.keys())

        purchase_moves = self._get_purchase_data(start_at, stop_at, product_ids)
        # product_ids |= purchase_moves.mapped('product_id')

        purchase_data = {}
        for move in purchase_moves:
            if move.product_id.id in purchase_data:
                purchase_data[move.product_id.id] |= move
            else:
                purchase_data[move.product_id.id] = move

        for product in product_ids:
            pd = {'0_qty': 0, '0_value': 0, '10_qty': 0, '10_value': 0, '20_qty': 0, '20_value': 0, '30_qty': 0, '30_value': 0, '40_qty': 0, '40_value': 0, '50_qty': 0, '50_value': 0, '60_qty': 0, '60_value': 0, '70_qty': 0, '70_value': 0, '70_up_qty': 0, '70_up_value': 0, 'net_sale_qty': 0, 'net_sale_value': 0}
            if pos_sale_data.get(product.id):
                product_sale_data = pos_sale_data[product.id]
                pd = self._get_sale_qty_value(product_sale_data)

            start_on = ''
            net_qty = 0
            if purchase_data.get(product.id):
                start_on = self.get_client_time(purchase_data[product.id][0].date)
                net_qty = sum(purchase_data[product.id].mapped('quantity_done'))
            size = ', '.join(product.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Size').mapped('name'))
            color = ', '.join(product.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Color').mapped('name'))
            data.append({
                'barcode': product.barcode or '',
                'product_code': product.default_code or '',
                'category': product.categ_id.name,
                'product_name': product.name,
                'size': ' - '.join(filter(None, [size, color])),
                'start_on': start_on,
                'net_qty': net_qty,
                '0_qty': pd['0_qty'],
                '0_value': pd['0_value'],
                '10_qty': pd['10_qty'],
                '10_value': pd['10_value'],
                '20_qty': pd['20_qty'],
                '20_value': pd['20_value'],
                '30_qty': pd['30_qty'],
                '30_value': pd['30_value'],
                '40_qty': pd['40_qty'],
                '40_value': pd['40_value'],
                '50_qty': pd['50_qty'],
                '50_value': pd['50_value'],
                '60_qty': pd['60_qty'],
                '60_value': pd['60_value'],
                '70_qty': pd['70_qty'],
                '70_value': pd['70_value'],
                '70_up_qty': pd['70_up_qty'],
                '70_up_value': pd['70_up_value'],
                'net_sale_qty': pd['net_sale_qty'],
                'net_sale_value': pd['net_sale_value'],
                'in_hand': product.qty_available,
                'in_transit': self._get_product_qty(product, 'transit'),
                'discount': 0,
            })
        return data

    def _get_sale_total(self, data):
        total_dict = {
            'net_qty': 0,
            '0_qty': 0,
            '0_value': 0,
            '10_qty': 0,
            '10_value': 0,
            '20_qty': 0,
            '20_value': 0,
            '30_qty': 0,
            '30_value': 0,
            '40_qty': 0,
            '40_value': 0,
            '50_qty': 0,
            '50_value': 0,
            '60_qty': 0,
            '60_value': 0,
            '70_qty': 0,
            '70_value': 0,
            '70_up_qty': 0,
            '70_up_value': 0,
            'net_sale_qty': 0,
            'net_sale_value': 0,
            'in_hand': 0,
            'in_transit': 0
        }
        for val in data:
            total_dict['net_qty'] += val['net_qty']
            total_dict['0_qty'] += val['0_qty']
            total_dict['0_value'] += val['0_value']
            total_dict['10_qty'] += val['10_qty']
            total_dict['10_value'] += val['10_value']
            total_dict['20_qty'] += val['20_qty']
            total_dict['20_value'] += val['20_value']
            total_dict['30_qty'] += val['30_qty']
            total_dict['30_value'] += val['30_value']
            total_dict['40_qty'] += val['40_qty']
            total_dict['40_value'] += val['40_value']
            total_dict['50_qty'] += val['50_qty']
            total_dict['50_value'] += val['50_value']
            total_dict['60_qty'] += val['60_qty']
            total_dict['60_value'] += val['60_value']
            total_dict['70_qty'] += val['70_qty']
            total_dict['70_value'] += val['70_value']
            total_dict['70_up_qty'] += val['70_up_qty']
            total_dict['70_up_value'] += val['70_up_value']
            total_dict['net_sale_qty'] += val['net_sale_qty']
            total_dict['net_sale_value'] += val['net_sale_value']
            total_dict['in_hand'] += val['in_hand']
            total_dict['in_transit'] += val['in_transit']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        category_ids = data.get('category_ids')
        product_ids = self.env['product.product'].browse(data.get('product_ids'))

        data = self._get_sale_data(start_at, stop_at, category_ids, product_ids)

        sheet = workbook.add_worksheet("Product Life Cycle Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format6 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '0.00'})
        format6.set_align('center')

        sheet.merge_range('A1:AB2', 'Product Life Cycle Report', format1)
        sheet.merge_range('A3:AB3', 'From : ' + start_at + ' To ' + stop_at , format5)
        sheet.write(3, 0, '', format2)
        sheet.write(3, 1, '', format2)
        sheet.write(3, 2, '', format2)
        sheet.write(3, 3, '', format2)
        sheet.write(3, 4, '', format2)
        sheet.merge_range('F4:G4', 'Purchase', format6)
        sheet.merge_range('H4:Y4', 'SALE ANALYSIS', format6)
        sheet.merge_range('Z4:AA4', 'Net Sale', format6)
        sheet.merge_range('AB4:AC4', 'Inventory Qty', format6)
        sheet.write(3, 29, 'Discount', format2)
        headers = ['Barcode', 'Internal Reference', 'Category', 'Product Name', 'Size/Color', 'Start On', 'Net Qty', '0% Qty', 'Sale Value', '10% Qty', 'Sale Value', '20% Qty', 'Sale Value', '30% Qty', 'Sale Value', '40% Qty', 'Sale Value', '50% Qty', 'Sale Value', '60% Qty', 'Sale Value', '70% Qty', 'Sale Value',  '>70% Qty', 'Sale Value', 'Qty', 'Sale Value', 'In-Hand', 'In-Transit', '%']
        row = 4
        col = 0
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 5
        col = 0
        for val in data:
            sheet.write(row, col+0, val['barcode'], format3)
            sheet.write(row, col+1, val['product_code'], format3)
            sheet.write(row, col+2, val['category'], format3)
            sheet.write(row, col+3, val['product_name'], format3)
            sheet.write(row, col+4, val['size'], format3)
            sheet.write(row, col+5, val['start_on'], format3)
            sheet.write(row, col+6, val['net_qty'], format3)
            sheet.write(row, col+7, val['0_qty'], format3)
            sheet.write(row, col+8, val['0_value'], format3)
            sheet.write(row, col+9, val['10_qty'], format3)
            sheet.write(row, col+10, val['10_value'], format3)
            sheet.write(row, col+11, val['20_qty'], format3)
            sheet.write(row, col+12, val['20_value'], format3)
            sheet.write(row, col+13, val['30_qty'], format3)
            sheet.write(row, col+14, val['30_value'], format3)
            sheet.write(row, col+15, val['40_qty'], format3)
            sheet.write(row, col+16, val['40_value'], format3)
            sheet.write(row, col+17, val['50_qty'], format3)
            sheet.write(row, col+18, val['50_value'], format3)
            sheet.write(row, col+19, val['60_qty'], format3)
            sheet.write(row, col+20, val['60_value'], format3)
            sheet.write(row, col+21, val['70_qty'], format3)
            sheet.write(row, col+22, val['70_value'], format3)
            sheet.write(row, col+23, val['70_up_qty'], format3)
            sheet.write(row, col+24, val['70_up_value'], format3)
            sheet.write(row, col+25, val['net_sale_qty'], format3)
            sheet.write(row, col+26, val['net_sale_value'], format3)
            sheet.write(row, col+27, val['in_hand'], format3)
            sheet.write(row, col+28, val['in_transit'], format3)
            sheet.write(row, col+29, val['discount'], format3)
            row += 1

        # Sheet Total
        total_dict = self._get_sale_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+6, total_dict['net_qty'], format4)
        sheet.write(row, col+7, total_dict['0_qty'], format4)
        sheet.write(row, col+8, total_dict['0_value'], format4)
        sheet.write(row, col+9, total_dict['10_qty'], format4)
        sheet.write(row, col+10, total_dict['10_value'], format4)
        sheet.write(row, col+11, total_dict['20_qty'], format4)
        sheet.write(row, col+12, total_dict['20_value'], format4)
        sheet.write(row, col+13, total_dict['30_qty'], format4)
        sheet.write(row, col+14, total_dict['30_value'], format4)
        sheet.write(row, col+15, total_dict['40_qty'], format4)
        sheet.write(row, col+16, total_dict['40_value'], format4)
        sheet.write(row, col+17, total_dict['50_qty'], format4)
        sheet.write(row, col+18, total_dict['50_value'], format4)
        sheet.write(row, col+19, total_dict['60_qty'], format4)
        sheet.write(row, col+20, total_dict['60_value'], format4)
        sheet.write(row, col+21, total_dict['70_qty'], format4)
        sheet.write(row, col+22, total_dict['70_value'], format4)
        sheet.write(row, col+23, total_dict['70_up_qty'], format4)
        sheet.write(row, col+24, total_dict['70_up_value'], format4)
        sheet.write(row, col+25, total_dict['net_sale_qty'], format4)
        sheet.write(row, col+26, total_dict['net_sale_value'], format4)
        sheet.write(row, col+27, total_dict['in_hand'], format4)
        sheet.write(row, col+28, total_dict['in_transit'], format4)
