# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import io
import re
import datetime
from odoo.tools.misc import xlwt
from odoo.exceptions import UserError
from odoo.tools import pycompat
from odoo.http import content_disposition, request
from odoo import http


class Controller(http.Controller):


    @http.route(['/pos_promotion_niq/product/export'], type='http', auth="user")
    def index(self, promotion_id):
        promotion_id = int(promotion_id)
        promotion = request.env['pos.promotion'].sudo().browse(promotion_id)
        columns_headers, promotion_data = promotion.web_export_promotion_product()

        return request.make_response(
            self.export_from_data(columns_headers, promotion_data),
            headers=[('Content-Disposition',
                    content_disposition('promotion_product.xls')),
                     ('Content-Type', 'application/vnd.ms-excel')],
            cookies={})

    def export_from_data(self, fields, rows):
        if len(rows) > 65535:
            raise UserError(_('There are too many rows (%s rows, limit: 65535) to export as Excel 97-2003 (.xls) format. Consider splitting the export.') % len(rows))

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')

        for i, fieldname in enumerate(fields):
            worksheet.write(0, i, fieldname)
            worksheet.col(i).width = 8000 # around 220 pixels

        base_style = xlwt.easyxf('align: wrap yes')
        date_style = xlwt.easyxf('align: wrap yes', num_format_str='YYYY-MM-DD')
        datetime_style = xlwt.easyxf('align: wrap yes', num_format_str='YYYY-MM-DD HH:mm:SS')

        for row_index, row in enumerate(rows):
            for cell_index, cell_value in enumerate(row):
                cell_style = base_style

                if isinstance(cell_value, bytes) and not isinstance(cell_value, str):
                    # because xls uses raw export, we can get a bytes object
                    # here. xlwt does not support bytes values in Python 3 ->
                    # assume this is base64 and decode to a string, if this
                    # fails note that you can't export
                    try:
                        cell_value = pycompat.to_text(cell_value)
                    except UnicodeDecodeError:
                        raise UserError(_("Binary fields can not be exported to Excel unless their content is base64-encoded. That does not seem to be the case for %s.") % fields[cell_index])

                if isinstance(cell_value, str):
                    cell_value = re.sub("\r", " ", pycompat.to_text(cell_value))
                elif isinstance(cell_value, datetime.datetime):
                    cell_style = datetime_style
                elif isinstance(cell_value, datetime.date):
                    cell_style = date_style
                worksheet.write(row_index + 1, cell_index, cell_value, cell_style)

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data
