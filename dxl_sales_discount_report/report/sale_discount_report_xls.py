# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
import pytz



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_sales_discount_report.sale_discount_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_pos_sale(self, line_ids):
        query = """ SELECT
            pol.product_id as product_id,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) >= 0 and (pol.discount + pol.promo_disc_percentage) <= 10 THEN sum(pol.price_subtotal) else 0.0 END as upto10,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 10 and (pol.discount + pol.promo_disc_percentage) <= 20 THEN sum(pol.price_subtotal) else 0.0 END as upto20,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 20 and (pol.discount + pol.promo_disc_percentage) <= 30 THEN sum(pol.price_subtotal) else 0.0 END as upto30,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 30 and (pol.discount + pol.promo_disc_percentage) <= 40 THEN sum(pol.price_subtotal) else 0.0 END as upto40,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 40 and (pol.discount + pol.promo_disc_percentage) <= 50 THEN sum(pol.price_subtotal) else 0.0 END as upto50,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 50 and (pol.discount + pol.promo_disc_percentage) <= 60 THEN sum(pol.price_subtotal) else 0.0 END as upto60,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 60 and (pol.discount + pol.promo_disc_percentage) <= 70 THEN sum(pol.price_subtotal) else 0.0 END as upto70,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 70 and (pol.discount + pol.promo_disc_percentage) <= 80 THEN sum(pol.price_subtotal) else 0.0 END as upto80,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 80 and (pol.discount + pol.promo_disc_percentage) <= 90 THEN sum(pol.price_subtotal) else 0.0 END as upto90,
            CASE WHEN (pol.discount + pol.promo_disc_percentage) > 90 and (pol.discount + pol.promo_disc_percentage) <= 100 THEN sum(pol.price_subtotal) else 0.0 END as upto100
            from pos_order_line as pol
            where id in %(line_ids)s
            group by pol.product_id, pol.discount, pol.promo_disc_percentage
        """
        self.env.cr.execute(query, {'line_ids': tuple(line_ids.ids)})
        return self._get_product_discount(self.env.cr.dictfetchall())

    def _get_product_discount(self, pos_data):
        product_data = {}
        for line in pos_data:
            product_id = line['product_id']
            if product_id in product_data:
                product_data[product_id].append(line)
            else:
                product_data[product_id] = [line]
        return product_data

    def _get_last_year_data(self, start_at, stop_at, shop_ids):
        start_at_last_year = datetime.strptime(start_at + ' 00:00:00', "%Y-%m-%d %H:%M:%S") - relativedelta(years=+1)
        stop_at_last_year = datetime.strptime(stop_at + ' 23:59:59', "%Y-%m-%d %H:%M:%S") - relativedelta(days=+1)
        domain = [
            ('create_date', '>=', start_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('create_date', '<=', stop_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('order_id.shop_id', 'in', shop_ids.ids)
        ]
        return self.env['pos.order.line'].sudo().search(domain)

    def _get_year_to_date(self, shop_ids):
        start_year_to_date = datetime.now().date().replace(month=1, day=1)
        start_at_last_year = datetime.strptime(start_year_to_date.strftime('%Y-%m-%d') + ' 00:00:00', "%Y-%m-%d %H:%M:%S") - relativedelta(years=+1)
        stop_at_last_year = datetime.strptime(datetime.now().strftime('%Y-%m-%d') + ' 23:59:59', "%Y-%m-%d %H:%M:%S") - relativedelta(days=+1)
        domain = [
            ('create_date', '>=', start_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('create_date', '<=', stop_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('order_id.shop_id', 'in', shop_ids.ids)
        ]
        return self.env['pos.order.line'].sudo().search(domain)

    def _get_previous_year_data(self, shop_ids):
        start_year_to_date = datetime.now().date().replace(month=1, day=1)
        end_year_to_date = datetime.now().date().replace(month=12, day=31)
        start_at_last_year = datetime.strptime(start_year_to_date.strftime('%Y-%m-%d') + ' 00:00:00', "%Y-%m-%d %H:%M:%S") - relativedelta(years=+1)
        stop_at_last_year = datetime.strptime(end_year_to_date.strftime('%Y-%m-%d') + ' 23:59:59', "%Y-%m-%d %H:%M:%S") - relativedelta(years=+1)
        domain = [
            ('create_date', '>=', start_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('create_date', '<=', stop_at_last_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('order_id.shop_id', 'in', shop_ids.ids)
        ]
        return self.env['pos.order.line'].sudo().search(domain)

    def _get_last_month_data(self, start_at, stop_at, shop_ids):
        start_at_month_year = datetime.strptime(start_at + ' 00:00:00', "%Y-%m-%d %H:%M:%S") - relativedelta(months=+1)
        stop_at_month_year = datetime.strptime(stop_at + ' 23:59:59', "%Y-%m-%d %H:%M:%S") - relativedelta(days=+1)
        domain = [
            ('create_date', '>=', start_at_month_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('create_date', '<=', stop_at_month_year.strftime('%Y-%m-%d %H:%M:%S')),
            ('order_id.shop_id', 'in', shop_ids.ids)
        ]
        return self.env['pos.order.line'].sudo().search(domain)

    def _get_sale_discount_data(self, start_at, stop_at, shop_ids):
        data = []
        domain = [
            ('create_date', '>=', start_at + ' 00:00:00'),
            ('create_date', '<=', stop_at + ' 23:59:59'),
            ('order_id.shop_id', 'in', shop_ids.ids)
        ]
        order_line_ids = self.env['pos.order.line'].sudo().search(domain)
        discunt_data = self._get_pos_sale(order_line_ids)
        product_ids = order_line_ids.mapped('product_id')
        lines_by_product = {}
        for line in order_line_ids:
            if line.product_id.id in lines_by_product:
                lines_by_product[line.product_id.id] |= line
            else:
                lines_by_product[line.product_id.id] = line
        # last_year_lines = self._get_last_year_data(start_at, stop_at, shop_ids)
        # year_to_date_lines = self._get_year_to_date(shop_ids)
        # last_year_data = self._get_previous_year_data(shop_ids)
        # last_month_lines = self._get_last_month_data(start_at, stop_at, shop_ids)
        s_no = 1
        for shop in shop_ids:
            for product in product_ids:
                product_lines = lines_by_product.get(product.id)
                # product_lines = order_line_ids.filtered(lambda x: x.product_id.id == product.id)
                gross_sales = sum([line.qty * line.price_unit for line in product_lines])
                sales_return = sum([line.qty * line.price_unit for line in product_lines.filtered(lambda x: x.qty < 0)])
                gst = sum([line.price_subtotal_incl - line.price_subtotal for line in product_lines])
                discount = sum([(line.qty * line.price_unit) - line.price_subtotal for line in product_lines])
                net_sales = sum([line.price_subtotal_incl for line in product_lines])
                disc_unit = sum([line.qty for line in product_lines if line.promo_disc_percentage > 0 or line.discount > 0])
                disc_amt = sum([line.price_subtotal for line in product_lines if line.promo_disc_percentage > 0 or line.discount > 0])
                fresh_unit = sum([line.qty for line in product_lines if line.promo_disc_percentage == 0 and line.discount == 0])
                fresh_amt = sum([line.price_subtotal for line in product_lines if line.promo_disc_percentage == 0 and line.discount == 0])
                disc_ratio = disc_amt * 100 / gross_sales if gross_sales > 0 else 0
                fresh_ratio = fresh_amt * 100 / gross_sales if gross_sales > 0 else 0

                # total_product_qty = disc_unit + fresh_unit
                # total_product_sale = disc_amt + fresh_amt

                # product_last_year_unit = sum([line.qty for line in last_year_lines.filtered(lambda x: x.product_id.id == product.id)])
                # unit_yoy = ((total_product_qty - product_last_year_unit) / product_last_year_unit) * 100

                # product_last_month_unit = sum([line.qty for line in last_month_lines.filtered(lambda x: x.product_id.id == product.id)])
                # unit_mom = ((total_product_qty - product_last_month_unit) / product_last_month_unit) * 100

                # year_to_date_qty = sum([line.qty for line in year_to_date_lines.filtered(lambda x: x.product_id.id == product.id)])
                # last_year_sale = sum([line.qty for line in last_year_data.filtered(lambda x: x.product_id.id == product.id)])
                # grow_ytd = ((year_to_date_qty - last_year_sale) / last_year_sale) * 100 if last_year_sale else 0
                # grow_period = ((total_product_qty - product_last_year_unit) / product_last_year_unit) * 100 if product_last_year_unit else 0

                # product_last_year_amt = sum([line.price_subtotal for line in last_year_lines.filtered(lambda x: x.product_id.id == product.id)])
                # product_last_month_amt = sum([line.price_subtotal for line in last_month_lines.filtered(lambda x: x.product_id.id == product.id)])
                # amt_yoy = ((total_product_sale - product_last_year_amt) / product_last_year_amt) * 100 if product_last_year_amt else 0
                # amt_mom = ((total_product_sale - product_last_month_amt) / product_last_month_amt) * 100 if product_last_month_amt else 0

                data.append({
                    's_no': s_no,
                    'shop_name': shop.name,
                    'product_name': product.name,
                    'gross_sales': gross_sales,
                    'sales_return': sales_return,
                    'gst': gst,
                    'discount': round(discount, 2),
                    'net_sales': net_sales,
                    'disc_unit': disc_unit,
                    'disc_amt': disc_amt,
                    'fresh_unit': fresh_unit,
                    'fresh_amt': fresh_amt,
                    'disc_ratio': disc_ratio,
                    'fresh_ratio': fresh_ratio,
                    # 'unit_yoy': unit_yoy,
                    # 'unit_mom': unit_mom,
                    # 'amt_yoy': amt_yoy,
                    # 'amt_mom': amt_mom,
                    # 'grow_ytd': grow_ytd,
                    # 'grow_period': grow_period,
                    # 'avg_ytd': 0,
                    # 'avg_period': 0,
                    'upto10': sum([line['upto10'] for line in discunt_data[product.id]]),
                    'upto20': sum([line['upto20'] for line in discunt_data[product.id]]),
                    'upto30': sum([line['upto30'] for line in discunt_data[product.id]]),
                    'upto40': sum([line['upto40'] for line in discunt_data[product.id]]),
                    'upto50': sum([line['upto50'] for line in discunt_data[product.id]]),
                    'upto60': sum([line['upto60'] for line in discunt_data[product.id]]),
                    'upto70': sum([line['upto70'] for line in discunt_data[product.id]]),
                    'upto80': sum([line['upto80'] for line in discunt_data[product.id]]),
                    'upto90': sum([line['upto90'] for line in discunt_data[product.id]]),
                    'upto100': sum([line['upto100'] for line in discunt_data[product.id]]),
                })
                s_no += 1
        return data

    def _get_sale_discount_total(self, data):
        total_dict = {
            'gross_sales': 0,
            'sales_return': 0,
            'gst': 0,
            'discount': 0,
            'net_sales': 0,
            'disc_unit': 0,
            'disc_amt': 0,
            'fresh_unit': 0,
            'fresh_amt': 0,
            'disc_ratio': 0,
            'fresh_ratio': 0,
            # 'unit_yoy': 0,
            # 'unit_mom': 0,
            # 'amt_yoy': 0,
            # 'amt_mom': 0,
            # 'grow_ytd': 0,
            # 'grow_period': 0,
            # 'avg_ytd': 0,
            # 'avg_period': 0,
            'upto10': 0,
            'upto20': 0,
            'upto30': 0,
            'upto40': 0,
            'upto50': 0,
            'upto60': 0,
            'upto70': 0,
            'upto80': 0,
            'upto90': 0,
            'upto100': 0,
        }
        for val in data:
            total_dict['gross_sales'] += val['gross_sales']
            total_dict['sales_return'] += val['sales_return']
            total_dict['gst'] += val['gst']
            total_dict['discount'] += val['discount']
            total_dict['net_sales'] += val['net_sales']
            total_dict['disc_unit'] += val['disc_unit']
            total_dict['disc_amt'] += val['disc_amt']
            total_dict['fresh_unit'] += val['fresh_unit']
            total_dict['fresh_amt'] += val['fresh_amt']
            total_dict['disc_ratio'] += val['disc_ratio']
            total_dict['fresh_ratio'] += val['fresh_ratio']
            # total_dict['unit_yoy'] += val['unit_yoy']
            # total_dict['unit_mom'] += val['unit_mom']
            # total_dict['amt_yoy'] += val['amt_yoy']
            # total_dict['amt_mom'] += val['amt_mom']
            # total_dict['grow_ytd'] += val['grow_ytd']
            # total_dict['grow_period'] += val['grow_period']
            # total_dict['avg_ytd'] += val['avg_ytd']
            # total_dict['avg_period'] += val['avg_period']
            total_dict['upto10'] += val['upto10']
            total_dict['upto20'] += val['upto20']
            total_dict['upto30'] += val['upto30']
            total_dict['upto40'] += val['upto40']
            total_dict['upto50'] += val['upto50']
            total_dict['upto60'] += val['upto60']
            total_dict['upto70'] += val['upto70']
            total_dict['upto80'] += val['upto80']
            total_dict['upto90'] += val['upto90']
            total_dict['upto100'] += val['upto100']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))

        data = self._get_sale_discount_data(start_at, stop_at, shop_ids)

        sheet = workbook.add_worksheet("Sales Report")
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

        sheet.merge_range('A1:N2', 'Sales Report', format1)
        sheet.merge_range('A3:N3', 'From : ' + start_at + ' To ' + stop_at , format5)

        sheet.merge_range('A4:A6', 'S.No.', format2)
        sheet.merge_range('B4:B6', 'POS Shop', format2)
        sheet.merge_range('C4:C6', 'Product Name', format2)
        sheet.merge_range('I4:N4', 'Contribution', format2)
        sheet.merge_range('I5:J5', 'Discounted Sale', format2)
        sheet.merge_range('K5:L5', 'Fresh Sale', format2)
        sheet.merge_range('M5:N5', 'Sales Contribution Ratio', format2)
        # sheet.merge_range('O4:V4', 'Analysis', format2)
        # sheet.merge_range('O5:P5', 'Contribution Base on Unit', format2)
        # sheet.merge_range('Q5:R5', 'Contribution Base on Amt', format2)
        # sheet.merge_range('S5:T5', 'Growth', format2)
        # sheet.merge_range('U5:V5', 'Avg. Selling Price', format2)
        sheet.merge_range('O4:X5', 'Discount Slab', format2)

        sheet.merge_range('D4:H5', 'Sales', format2)


        headers = ['Gross Sales', 'Sales Return', 'GST', 'Discount', 'Net Sales', 'Unit', 'Amt', 'Unit', 'Amt', 'Discounted %', 'Fresh  %', 'Upto 10%', 'Upto 20%', 'Upto 30%', 'Upto 40%', 'Upto 50%', 'Upto 60%', 'Upto 70%', 'Upto 80%', 'Upto 90%', 'Upto 100%']
        
        row = 5
        col = 3
        for header in headers:
            sheet.set_column(col, 1, 13)
            sheet.write(row, col, header, format2)
            col += 1

        row = 6
        col = 0
        for val in data:
            sheet.write(row, col+0, val['s_no'], format6)
            sheet.write(row, col+1, val['shop_name'], format3)
            sheet.write(row, col+2, val['product_name'], format3)
            sheet.write(row, col+3, val['gross_sales'], format3)
            sheet.write(row, col+4, val['sales_return'], format6)
            sheet.write(row, col+5, val['gst'], format6)
            sheet.write(row, col+6, val['discount'], format3)
            sheet.write(row, col+7, val['net_sales'], format3)
            sheet.write(row, col+8, val['disc_unit'], format3)
            sheet.write(row, col+9, val['disc_amt'], format3)
            sheet.write(row, col+10, val['fresh_unit'], format3)
            sheet.write(row, col+11, val['fresh_amt'], format3)
            sheet.write(row, col+12, val['disc_ratio'], format3)
            sheet.write(row, col+13, val['fresh_ratio'], format3)
            # sheet.write(row, col+14, val['unit_yoy'], format3)
            # sheet.write(row, col+15, val['unit_mom'], format3)
            # sheet.write(row, col+16, val['amt_yoy'], format3)
            # sheet.write(row, col+17, val['amt_mom'], format3)
            # sheet.write(row, col+18, val['grow_ytd'], format3)
            # sheet.write(row, col+19, val['grow_period'], format3)
            # sheet.write(row, col+20, val['avg_ytd'], format3)
            # sheet.write(row, col+21, val['avg_period'], format3)
            sheet.write(row, col+14, val['upto10'], format3)
            sheet.write(row, col+15, val['upto20'], format3)
            sheet.write(row, col+16, val['upto30'], format3)
            sheet.write(row, col+17, val['upto40'], format3)
            sheet.write(row, col+18, val['upto50'], format3)
            sheet.write(row, col+19, val['upto60'], format3)
            sheet.write(row, col+20, val['upto70'], format3)
            sheet.write(row, col+21, val['upto80'], format3)
            sheet.write(row, col+22, val['upto90'], format3)
            sheet.write(row, col+23, val['upto100'], format3)
            row += 1

        # # Sheet Total
        total_dict = self._get_sale_discount_total(data)
        row += 1
        sheet.write(row, col+0, 'Total', format5)
        sheet.write(row, col+3, total_dict['gross_sales'], format7)
        sheet.write(row, col+4, total_dict['sales_return'], format7)
        sheet.write(row, col+5, total_dict['gst'], format4)
        sheet.write(row, col+6, total_dict['discount'], format4)
        sheet.write(row, col+7, total_dict['net_sales'], format4)
        sheet.write(row, col+8, total_dict['disc_unit'], format4)
        sheet.write(row, col+9, total_dict['disc_amt'], format4)
        sheet.write(row, col+10, total_dict['fresh_unit'], format4)
        sheet.write(row, col+11, total_dict['fresh_amt'], format4)
        sheet.write(row, col+12, total_dict['disc_ratio'], format4)
        sheet.write(row, col+13, total_dict['fresh_ratio'], format4)
        # sheet.write(row, col+14, total_dict['unit_yoy'], format4)
        # sheet.write(row, col+15, total_dict['unit_mom'], format4)
        # sheet.write(row, col+16, total_dict['amt_yoy'], format4)
        # sheet.write(row, col+17, total_dict['amt_mom'], format4)
        # sheet.write(row, col+18, total_dict['grow_ytd'], format4)
        # sheet.write(row, col+19, total_dict['grow_period'], format4)
        # sheet.write(row, col+20, total_dict['avg_ytd'], format4)
        # sheet.write(row, col+21, total_dict['avg_period'], format4)
        sheet.write(row, col+14, total_dict['upto10'], format4)
        sheet.write(row, col+15, total_dict['upto20'], format4)
        sheet.write(row, col+16, total_dict['upto30'], format4)
        sheet.write(row, col+17, total_dict['upto40'], format4)
        sheet.write(row, col+18, total_dict['upto50'], format4)
        sheet.write(row, col+19, total_dict['upto60'], format4)
        sheet.write(row, col+20, total_dict['upto70'], format4)
        sheet.write(row, col+21, total_dict['upto80'], format4)
        sheet.write(row, col+22, total_dict['upto90'], format4)
        sheet.write(row, col+23, total_dict['upto100'], format4)
