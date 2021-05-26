# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime



class ProductXlsx(models.AbstractModel):
    _name = 'report.dxl_sales_summary_report.sale_summary_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_product_sale(self, start_at, stop_at, shop_ids, product_ids):
        query = """SELECT p.id as product_id,
                        s.id as shop_id,
                        sum(pol.qty) as sale_qty,
                        sum(pol.price_subtotal_incl) as sale_amount,
                        p.barcode as barcode,
                        p.default_code as default_code
                        FROM pos_order_line AS pol
                        left join product_product as p on (p.id = pol.product_id)
                        left join product_template as pt on (pt.id = p.product_tmpl_id)
                        left join pos_order as po on (po.id = pol.order_id)
                        left join pos_multi_shop as s on (s.id = po.shop_id)
                        WHERE
                        po.date_order >= %(start_at)s
                        and po.date_order <= %(stop_at)s
                        and po.shop_id in %(shop_ids)s
                        and pol.product_id in %(product_ids)s
                        and pol.qty != 0.0
                        GROUP BY p.id, s.id
        """
        self.env.cr.execute(query , {'start_at': start_at + ' 00:00:00', 'stop_at': stop_at + ' 23:59:59', 'shop_ids': tuple(shop_ids.ids), 'product_ids': tuple(product_ids.ids)})
        result = self.env.cr.dictfetchall()
        shop_data = {}
        for res in result:
            if res['shop_id'] in shop_data:
                shop_data[res['shop_id']].append(res)
            else:
                shop_data[res['shop_id']] = [res]

        product_data = {}
        for product in product_ids:
            color = ''
            size = ''
            for pav_id in product.product_template_attribute_value_ids:
                if pav_id.attribute_id.name == 'Color':
                    color = pav_id.name
                if pav_id.attribute_id.name == 'Size':
                    size = pav_id.name
            product_data[product.id] = {
                'categ_name': product.categ_id.name,
                'product_name': product.name,
                'color': color,
                'size': size,
                'cost': product.standard_price,
            }
        return shop_data, product_data

    def _get_sale_total(self, data):
        total_dict = {'sale_qty': 0, 'sale_amount': 0, 'cost': 0}
        for val in data:
            total_dict['sale_qty'] += val['sale_qty']
            total_dict['sale_amount'] += val['sale_amount']
            total_dict['cost'] += val['cost']
        return total_dict

    def generate_xlsx_report(self, workbook, data, products):
        start_at = data.get('start_at')
        stop_at = data.get('stop_at')
        shop_ids = self.env['pos.multi.shop'].browse(data.get('shop_ids'))
        category_ids = data.get('category_ids')
        product_ids = self.env['product.product'].browse(data.get('product_ids'))

        sheet = workbook.add_worksheet("Sale Summary Report")
        format1 = workbook.add_format({'font_size': 15})
        format2 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        format3 = workbook.add_format({'font_size': 10})
        format5 = workbook.add_format({'font_size': 10, 'bold': True})
        format6 = workbook.add_format({'font_size': 10, 'bold': True, 'bg_color': '#D3D3D3', 'border':1})
        num_format = workbook.add_format({'font_size': 10, 'num_format': '0.00'})
        format4 = workbook.add_format({'font_size': 10, 'top': 1, 'bottom': 6, 'num_format': '0.00'})
        format1.set_align('center')
        format6.set_align('center')

        sheet.merge_range('A1:I2', 'Sale Summary Report', format1)
        headers = ["Barcode", "Product Category", "Internal Reference", "Product Name", "Color", 'Size', 'Sale Quantity', 'Sale Amount', 'Cost']
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

        shop_data, product_data = self._get_product_sale(start_at, stop_at, shop_ids, product_ids)
        for shop in shop_ids:
            s_data = shop_data.get(shop.id)
            if not s_data:
                continue
            sheet.merge_range(row+1, 0, row+1, 8, shop.name, format6)
            row += 2
            col = 0
            sale_qty = 0.0
            sale_amount = 0.0
            cost = 0.0
            for line in s_data:
                val = product_data[line.get('product_id')]
                sheet.write(row, col+0, line['barcode'], format3)
                sheet.write(row, col+1, val['categ_name'], format3)
                sheet.write(row, col+2, line['default_code'], format3)
                sheet.write(row, col+3, val['product_name'], format3)
                sheet.write(row, col+4, val['color'], format3)
                sheet.write(row, col+5, val['size'], num_format)
                sheet.write(row, col+6, line['sale_qty'], num_format)
                sheet.write(row, col+7, line['sale_amount'], num_format)
                sheet.write(row, col+8, val['cost'], num_format)
                sale_qty += line['sale_qty']
                sale_amount += line['sale_amount']
                cost += val['cost']
                row += 1

            # Sheet Total
            row += 1
            sheet.write(row, col+4, 'Total', format5)
            sheet.write(row, col+6, sale_qty, format4)
            sheet.write(row, col+7, sale_amount, format4)
            sheet.write(row, col+8, cost, format4)
