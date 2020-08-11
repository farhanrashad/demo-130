# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlwt
import base64
from io import StringIO
from odoo import api, fields, models, _
import platform
import time
from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta

class WizardWizards(models.Model):
    _name = 'wizard.reports'
    _description = 'Helpdesk Ticket Details'
    
    date_from = fields.Date('Date From:',default=time.strftime('%Y-%m-01'))
    date_to = fields.Date('Date To:',default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],)
    
    stage = fields.Many2one('helpdesk.ticket.stage', string="Stage")
    
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'helpdesk.ticket'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('de_sap_ticket_details_report.stock_xlsx').report_action(self, data=datas)


class StockReportXls(models.AbstractModel):
    _name = 'report.de_sap_ticket_details_report.stock_report_xls'
    _inherit = 'report.report_xlsx.abstract'
    
    

    def action_purchase_report(self,data):
#XLS report

        lines = []
        lval = []
        
        if(data['form']['date_from'] and  data['form']['date_to']  is not False):
                 
                carpt_pur=self.env['helpdesk.ticket'].search([
                                                            ('create_date.date','>=',data['form']['date_from']),
                                                            ('create_date.date','<=',data['form']['date_to']),
                                                            ('stage_id','==',data['form']['stage'])
                                                             ]) 
                   
                for cp in carpt_pur:
                    if cp:
                        lines.append(cp)    
                 
                 
                lval.append(('create_date.date','>=',data['form']['date_from']))
                lval.append(('create_date.date','<=',data['form']['date_to'])) 
                lval.append(('stage_id','<=',data['form']['stage']))  
        workbook = xlwt.Workbook()
        for rec in lval:
            purchase = []
            product = {}
            product ['crmid'] = rec.product_id.name
            product ['number'] = rec.product_qty
            product ['material'] = rec.qty_received
            product ['customer_model_desc'] = rec.qty_invoiced
            product ['contact_name'] = rec.price_unit
            product ['contact_no'] = rec.taxes_id.name
            product ['site_address'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['material'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['distributor'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['city'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol
            product ['description'] = str(rec.price_subtotal)+' '+rec.currency_id.symbol

            purchase.append(product)


            style0 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz right;', num_format_str='#,##0.00')
            style1 = xlwt.easyxf('font: name Times New Roman bold on; pattern: pattern solid, fore_colour black;align: horiz center;', num_format_str='#,##0.00')
            style2 = xlwt.easyxf('font:height 400,bold True; pattern: pattern solid, fore_colour black;', num_format_str='#,##0.00')
            style3 = xlwt.easyxf('font:bold True;', num_format_str='#,##0.00')
            style4 = xlwt.easyxf('font:bold True;  borders:top double;align: horiz right;', num_format_str='#,##0.00')
            style5 = xlwt.easyxf('font: name Times New Roman bold on;align: horiz center;', num_format_str='#,##0')
            style6 = xlwt.easyxf('font: name Times New Roman bold on;', num_format_str='#,##0.00')
            style7 = xlwt.easyxf('font:bold True;  borders:top double;', num_format_str='#,##0.00')


            sheet = workbook.add_sheet(rec.name)

            sheet.write_merge(2, 3, 4, 6, 'Purchase   Order :', style2)
            sheet.write_merge(2, 3, 7, 8, purchase['partner_no'], style2)
            sheet.write(5, 1, 'Vendor', style3)
            sheet.write(5, 2, purchase['partner_id'], style0)
            sheet.write_merge(5, 5, 8, 9, 'Order  Date', style3)
            sheet.write_merge(5, 5, 10, 11, purchase['date_order'], style0)
            sheet.write_merge(6, 6, 8, 9, 'Vendor Reference', style3)
            sheet.write_merge(6, 6, 10, 11, purchase['partner_ref'], style0)
            sheet.write_merge(7, 7, 8, 9, 'Payment Terms', style3)
            sheet.write_merge(7, 7, 10, 11, purchase['payment_term_id'], style0)

            sheet.write(10, 1, 'S NO', style1)
            sheet.write_merge(10, 10, 2, 3, 'PRODUCT', style1)
            sheet.write_merge(10, 10, 4, 5, 'QUANTITY', style1)
            sheet.write_merge(10, 10, 6, 7, 'UNIT PRICE', style1)
            sheet.write_merge(10, 10, 8, 10, 'TAXES', style1)
            sheet.write(10, 11, 'SUBTOTAL', style1)

            n = 11; i = 1
            for product in purchase['products']:
                sheet.write(n, 1, i, style5)
                sheet.write_merge(n, n, 2, 3, product['product_id'], style6)
                sheet.write_merge(n, n, 4, 5, product['product_qty'], style0)
                sheet.write_merge(n, n, 6, 7, product['price_unit'], style0)
                sheet.write_merge(n, n, 8, 10, product['taxes_id'], style0)
                sheet.write(n, 11, product['price_subtotal'], style0)
                n += 1; i += 1
            sheet.write_merge(n+1, n+1, 9, 10, 'Untaxed Amount', style7)
            sheet.write(n+1, 11, purchase['amount_untaxed'], style4)
            sheet.write_merge(n+2, n+2, 9, 10, 'Taxes', style7)
            sheet.write(n+2, 11, purchase['amount_tax'], style4)
            sheet.write_merge(n+3, n+3, 9, 10, 'Total', style7)
            sheet.write(n+3, 11, purchase['amount_total'], style4)
