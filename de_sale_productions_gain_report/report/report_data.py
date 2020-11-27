# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import dateutil


class ReportData(models.AbstractModel):
    _name = 'report.de_sale_productions_gain_report.report_production_gain_template'
    _description = 'Report Data'

    def get_product_obj(self, date1, date2):
        obj = date(date2) - date(date1) 
        return obj.days
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        values = []
        small_list = []
        large_list = []
        register_ids = self.env.context.get('active_ids', [])
        contrib_registers = self.env['sale.order'].browse(register_ids)
        print('start', data['form'].get('date'))
        non_converted = str(data['form'].get('date'))
        converted_date = dateutil.parser.parse(non_converted).date()
        print('non', converted_date)
        date_from = data['form'].get('date', fields.Date.today())
        date_to = data['form'].get('date', str(datetime.now() + relativedelta(months=+1, day=1, days=-1))[:10])
        order = data['form'].get('proforma_invoice_no')
        order_id = order[0]
        order_lines = self.env['sale.order.line'].search([('order_id', '=', order_id)])
        for a1 in order_lines:
            values.append(a1.product_id.product_tmpl_id.id)
            values = list(dict.fromkeys(values))
        for value in values:
            # print('value', value.name)
            for line in order_lines:
                if line.product_id.product_tmpl_id.id == value:
                    small_list.append(line.product_id.id)
        return {
            'doc_ids': register_ids,
            'doc_model': 'sale.order',
            'docs': contrib_registers,
            'data': data,
            'values': values,
            'get_product_obj':self.get_product_obj,
            # 'lines_data': lines_data,
            # 'lines_total': lines_total
        }


