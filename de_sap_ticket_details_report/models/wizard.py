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
        for rec in order:
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

            custom_value['products'] = purchase
            custom_value ['partner_id'] = rec.partner_id.name
            custom_value ['partner_ref'] = rec.partner_ref
            custom_value ['payment_term_id'] = rec.payment_term_id.name
            custom_value ['date_order'] = rec.date_order
            custom_value ['partner_no'] = rec.name
            custom_value ['amount_total'] = str(rec.amount_total)+' '+rec.currency_id.symbol
            custom_value ['amount_untaxed'] = str(rec.amount_untaxed)+' '+rec.currency_id.symbol
            custom_value ['amount_tax'] = str(rec.amount_tax)+' '+rec.currency_id.symbol

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
            sheet.write_merge(2, 3, 7, 8, custom_value['partner_no'], style2)
            sheet.write(5, 1, 'Vendor', style3)
            sheet.write(5, 2, custom_value['partner_id'], style0)
            sheet.write_merge(5, 5, 8, 9, 'Order  Date', style3)
            sheet.write_merge(5, 5, 10, 11, custom_value['date_order'], style0)
            sheet.write_merge(6, 6, 8, 9, 'Vendor Reference', style3)
            sheet.write_merge(6, 6, 10, 11, custom_value['partner_ref'], style0)
            sheet.write_merge(7, 7, 8, 9, 'Payment Terms', style3)
            sheet.write_merge(7, 7, 10, 11, custom_value['payment_term_id'], style0)

            sheet.write(10, 1, 'S NO', style1)
            sheet.write_merge(10, 10, 2, 3, 'PRODUCT', style1)
            sheet.write_merge(10, 10, 4, 5, 'QUANTITY', style1)
            sheet.write_merge(10, 10, 6, 7, 'UNIT PRICE', style1)
            sheet.write_merge(10, 10, 8, 10, 'TAXES', style1)
            sheet.write(10, 11, 'SUBTOTAL', style1)

            n = 11; i = 1
            for product in custom_value['products']:
                sheet.write(n, 1, i, style5)
                sheet.write_merge(n, n, 2, 3, product['product_id'], style6)
                sheet.write_merge(n, n, 4, 5, product['product_qty'], style0)
                sheet.write_merge(n, n, 6, 7, product['price_unit'], style0)
                sheet.write_merge(n, n, 8, 10, product['taxes_id'], style0)
                sheet.write(n, 11, product['price_subtotal'], style0)
                n += 1; i += 1
            sheet.write_merge(n+1, n+1, 9, 10, 'Untaxed Amount', style7)
            sheet.write(n+1, 11, custom_value['amount_untaxed'], style4)
            sheet.write_merge(n+2, n+2, 9, 10, 'Taxes', style7)
            sheet.write(n+2, 11, custom_value['amount_tax'], style4)
            sheet.write_merge(n+3, n+3, 9, 10, 'Total', style7)
            sheet.write(n+3, 11, custom_value['amount_total'], style4)
#CSV report
        datas = []
        for values in order:
            for value in values.order_line:
                if value.product_id.seller_ids:
                    item = [
                            str(value.order_id.name or ''),
                            str(''),
                            str(''),
                            str(value.product_id.barcode or ''),
                            str(value.product_id.default_code or ''),
                            str(value.product_id.name or ''),
                            str(value.product_qty or ''),
                            str(value.product_id.seller_ids[0].product_code or ''),
                            str(value.partner_id.title or ''),
                            str(value.partner_id.name or ''),
                            str(value.partner_id.email or ''),
                            str(value.partner_id.phone or ''),
                            str(value.partner_id.mobile or ''),
                            str(value.partner_id.street or ''),
                            str(value.partner_id.street2 or ''),
                            str(value.partner_id.zip or ''),
                            str(value.partner_id.city or ''),
                            str(value.partner_id.country_id.name or ' '),
                            ]
                    datas.append(item)


    def get_lines(self, data):
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
 
#         else:
#             if data['form']['location']:
#                 stock_history = self.env['product.product'].search([('stock_quant_ids.location_id','in',data['form']['location'])])
#             
#             else:
        else:
            stock_history = self.env['product.product'].search([])
        
            
        for obj in stock_history:
            sale_value = 0
            purchase_value = 0
           
#             product = self.env['product.product'].search([('id','=',obj.id),('create_date','<=',data['form']['date_from'])])
            product = self.env['product.product'].search([('id','=',obj.id)])

            
           
            
#             pr_hist =self.env['stock.history'].search([('product_id','=',obj.id),('move_id.location_id.usage','=','supplier'),('date','>=',data['form']['date_from']),('date','<=',data['form']['date_to'])])
#             pr_hist =self.env['purchase.order.line'].search([('product_id','=',obj.id),('state','=','done'),('date_planned','>=',data['form']['date_from']),('date_planned','<=',data['form']['date_to'])])
            pr_hist =self.env['stock.pack.operation'].search([('product_id','=',obj.id),('state','=','done'),('picking_id.location_id','in',location),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to']),('location_dest_id','in',location)])
            pr_hist = pr_hist.filtered(lambda r: r.from_loc == 'Vendors')
            
            pr_return_hist =self.env['stock.pack.operation'].search([('product_id','=',obj.id),('state','=','done'),('picking_id.location_id','in',location),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to']),('location_dest_id','in',location)])
            pr_return_hist = pr_return_hist.filtered(lambda r: r.to_loc == 'Vendors')
            
#             production_hist = self.env['stock.history'].search([('product_id','=',obj.id),('move_id.location_id.usage','=','production')])
            production_hist = self.env['mrp.production'].search([('location_dest_id','in',location),('product_id','=',obj.id),('date_planned_start','>=',data['form']['date_from']),('date_planned_start','<=',data['form']['date_to'])])
#             sales_hist = self.env['sale.order.line'].search([('product_id','=',obj.id),('state','=','done'),('order_id.confirmation_date','>=',data['form']['date_from']),('order_id.confirmation_date','<=',data['form']['date_to'])])
#             sales_hist = self.env['product.product'].search([('id','=',obj.id)]).stock_quant_ids #self.env['stock.history'].search([('product_id','=',obj.id)])
            sales_hist = self.env['stock.pack.operation'].search([('product_id','=',obj.id),('state','=','done'),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to']),('location_dest_id','in',location),('picking_id.location_id','in',location),])
            sales_hist = sales_hist.filtered(lambda r: r.to_loc == 'Customers')
            
            return_sales = self.env['stock.pack.operation'].search([('product_id','=',obj.id),('state','=','done'),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to']),('location_dest_id','in',location),('picking_id.location_id','in',location),])
            return_sales = return_sales.filtered(lambda r: r.from_loc == 'Customers')
#             issue_sale_stock_produ = self.env['stock.history'].search([('product_id','=',obj.id),('move_id.location_id.usage','=','internal'),('move_id.quant_ids.location_id.usage','=','production')])
#             issue_sale_stock_produ = self.env['sale.order.line'].search([('product_id','=',obj.id),('state','=','done'),('order_id.confirmation_date','>=',data['form']['date_from']),('order_id.confirmation_date','<=',data['form']['date_to'])])
            issue_sale_stock_produ = self.env['stock.move'].search([('product_id','=',obj.id),('location_id','in',location),('location_dest_id','in',location),('raw_material_production_id.date_planned_start','>=',data['form']['date_from']),('raw_material_production_id.date_planned_start','<=',data['form']['date_to'])])
#             all_trnsfr_in = self.env['stock.move'].search([('product_id','=',obj.id),('picking_id.location_id.usage','=','inventory'),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to'])])
#             all_trnsfr_out = self.env['stock.move'].search([('product_id','=',obj.id),('picking_id.location_dest_id.usage','=','inventory'),('picking_id.min_date','>=',data['form']['date_from']),('picking_id.min_date','<=',data['form']['date_to'])])
            all_trnsfr_in = self.env['stock.move'].search([('product_id','=',obj.id),('location_id.usage','=','inventory'),('location_dest_id','in',location),('date','>=',data['form']['date_from']),('date','<=',data['form']['date_to'])])
            all_trnsfr_out = self.env['stock.move'].search([('product_id','=',obj.id),('location_dest_id.usage','=','inventory'),('location_dest_id','in',location),('date','>=',data['form']['date_from']),('date','<=',data['form']['date_to'])])
            
            all_trn_in =0
            all_trn_out =0
            all_transfr =0
            return_pur =0
            purchase=0
            return_sale=0
            sales=0
            production=0
            issue_sale=0
            adjustment=0
            
#             for issp in issue_sale_stock_produ:
# #                 sales = sales + issp.product_uom_qty
#                 issue_sale = issue_sale+issp.product_uom_qty
           
            for issp in issue_sale_stock_produ:
#                 move_id.
                issue_sale = issue_sale+issp.product_uom_qty
                
            for smov in pr_return_hist:
                return_pur =  return_pur + smov.qty_done
                
            for smov in pr_hist:
                purchase = purchase + smov.qty_done
            purchase = purchase - return_pur  
#                 
            for smov in production_hist:
                production = production + smov.product_qty
#                 production = production + smov.move_id.product_qty
             
            for smov in return_sales:
                return_sale = return_sale + smov.qty_done 
                                    
            for smov in sales_hist:
                sales = sales + smov.qty_done 
            sales = sales - return_sale
            
            
            for trsfr in all_trnsfr_in:
                all_trn_in = all_trn_in + trsfr.product_uom_qty
                # print trsfr.name
                # print trsfr.product_uom_qty
            for trsfr_out in all_trnsfr_out:
#                 move_id.
                all_trn_out = all_trn_out + trsfr_out.product_uom_qty 
       
            all_transfr = all_trn_in - all_trn_out
             
       
#             adjustment is really transfer
            ob = self.get_ob(obj,data['form']['date_from'],location,data['form']['product'])
            cb = self.get_cb(obj,data['form']['date_to'],location,data['form']['product'])
# - cb
            adjustment =  -1*(ob + purchase  + production + all_transfr - issue_sale - sales -cb)
            

           
                
            sale_obj = self.env['sale.order.line'].search([('order_id.state', '=', 'done'),
                                                           ('product_id', '=', product.id),
                                                           ('order_id.warehouse_id', '=', warehouse)])
            for i in sale_obj:
                sale_value = sale_value + i.product_uom_qty
            purchase_obj = self.env['purchase.order.line'].search([('order_id.state', '=', 'done'),('product_id', '=', product.id),('order_id.picking_type_id', '=', warehouse),('date_planned','>=',data['form']['date_from']),('date_planned','<=',data['form']['date_to'])])
            for i in purchase_obj:
                purchase_value = purchase_value + i.product_qty
            
            
            
#             print loc
            if(sales != 0 or purchase!=0 or self.get_ob(obj,data['form']['date_from'],location,data['form']['product']) !=0 or
               self.get_cb(obj,data['form']['date_to'],location,data['form']['product']) !=0 or all_transfr !=0 or production!=0 or issue_sale !=0 or adjustment != 0):
                if(data['form']['check'] == True):
                    vals = {
                        'sku': obj.default_code,
                        'name': obj.name+' '+obj.attribute_value_ids.name,
                        'category': obj.categ_id.name,
                        'sale_value': sales*obj.standard_price,#product.sales_count,
                        'purchase_value':purchase*obj.standard_price, #product.purchase_count, 
                        'ob': self.get_ob(obj,data['form']['date_from'],location,data['form']['product'])*obj.standard_price,#product.with_context({'warehouse': warehouse}).qty_available,
                        'cb': self.get_cb(obj,data['form']['date_to'],location,data['form']['product'])*obj.standard_price,#product_close.with_context({'warehouse': warehouse}).qty_available,
                        
                        
                        'adjustment':all_transfr*obj.standard_price,#adjustment,#sumadj,
                        'production':production*obj.standard_price,
                        'issue_sale':issue_sale*obj.standard_price,
                        'transfers':adjustment*obj.standard_price,
                    }
                    lines.append(vals)
                else:
                    print(str(obj.name))
                    print(str(obj.attribute_value_ids.name))
                    vals = {
                    'sku': obj.default_code,
                    'name': (str(obj.name))+' '+(str(obj.attribute_value_ids.name) ),
                    'category': obj.categ_id.name,
                    'sale_value': sales,#product.sales_count,
                    'purchase_value':purchase, #product.purchase_count, 
                    'ob': self.get_ob(obj,data['form']['date_from'],location,data['form']['product']),#product.with_context({'warehouse': warehouse}).qty_available,
                    'cb': self.get_cb(obj,data['form']['date_to'],location,data['form']['product']),#product_close.with_context({'warehouse': warehouse}).qty_available,

                    
                    'adjustment':all_transfr,#adjustment,#sumadj,
                    'production':production,
                    'issue_sale':issue_sale,
                    'transfers':adjustment,
                }
                    lines.append(vals)
    
        return lines


    def generate_xlsx_report(self, data):
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        formatblack = workbook.add_format({'font_size': 8, 'align': 'center', 'right': True, 'left': True,'bottom': True, 'top': True, 'bold': True})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        underline = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True, 'bold': True,'underline':True})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')#                         sheet.write(prod_row, prod_col + 4, each['cost_price'], font_size_8)
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        sheet.merge_range('A2:G2', 'Brand Wise Summary of Stock Movement', underline)
        sheet.merge_range('A3:G3', 'Period From: ' + data['form']['date_from']+' To '+data['form']['date_to'], font_size_8)        
#         sheet.merge_range(2, 7, 2, count, 'Warehouses', format1)
        sheet.merge_range(2, 7, 2,'Warehouses', format1)

        
        
        def footertable():
            return
        
        def headertable(prod_row):
            print('sss')
            print(data1)
            sheet.merge_range('A'+str(prod_row)+':B'+str(prod_row), 'Category', format21)
            w_col_no = 6
            w_col_no1 = 7
            for i in get_warehouse[0]:
                w_col_no = w_col_no + 11
                sheet.merge_range(3, w_col_no1, 3, w_col_no, i, format11)
                w_col_no1 = w_col_no1 + 11
            sheet.merge_range(prod_row+1, 0,prod_row,0, 'Code', format21)
            sheet.merge_range(prod_row+1, 1, prod_row, 3, 'Name', format21)

            p_col_no1 = 4
            p_col_inc = 10
            for i in get_warehouse[0]:
                if(data1['form']['check'] == True):
                    sheet.merge_range(prod_row+1, p_col_no1,prod_row, p_col_no1+1, 'Opening Balance/Rs', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 2,prod_row, p_col_no1+3, 'Purchase/Rs', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 4,prod_row, p_col_no1+5, 'Production/Rs', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 6,prod_row, p_col_no1+7, 'Transfers/Rs', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 8,prod_row, p_col_no1+9, 'Adjustments (+/-)/Rs', format21)
                  
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc, prod_row+1, p_col_no1 + p_col_inc+1, 'Issue to Production/Rs', format21)
                    
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc+2, prod_row+1, p_col_no1 + p_col_inc+3, 'Sale/Rs', format21)
    
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc+4, prod_row+1, p_col_no1 + p_col_inc+5,  'Closing Balance/Rs', format21)

                    
                else:
                    sheet.merge_range(prod_row+1, p_col_no1,prod_row, p_col_no1+1, 'Opening Balance', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 2,prod_row, p_col_no1+3, 'Purchase', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 4,prod_row, p_col_no1+5, 'Production', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 6,prod_row, p_col_no1+7, 'Transfers', format21)
                    sheet.merge_range(prod_row+1, p_col_no1 + 8,prod_row, p_col_no1+9, 'Adjustments (+/-)', format21)
                  
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc, prod_row+1, p_col_no1 + p_col_inc+1, 'Issue to Production', format21)
                    
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc+2, prod_row+1, p_col_no1 + p_col_inc+3, 'Sale', format21)
    
                    sheet.merge_range(prod_row, p_col_no1 + p_col_inc+4, prod_row+1, p_col_no1 + p_col_inc+5,  'Closing Balance', format21)

                p_col_no1 = p_col_no1 + 11
            
      
        
                
#             Loading data
        prod_row =6
        prod_col = 0
        headertable(prod_row-1)
        
        headertable(5)
        for i in get_warehouse[1]:
            
            get_line = self.get_lines(data, i)
#             if not get_line:
#                 get_line = self.parentline(data, i)
            
            rem_dup = set()
            for ech in get_line:
                if ech['category'] not in rem_dup:
                    rem_dup.add(ech['category'])
                else:
                    pass
            for uniq in rem_dup:
                check=0
                headertable(prod_row-1)
                for each in get_line:
                      
                    if each['category'] == uniq:  
                        if(check < 1):
                            sheet.merge_range('C'+str(prod_row-1)+':F'+str(prod_row-1) ,each['category'], format21)
                            check = check +1   
                        sheet.write(prod_row+1, prod_col, each['sku'], font_size_8)
                        sheet.merge_range(prod_row+1, prod_col + 1, prod_row+1, prod_col + 3, each['name'], font_size_8)
                          
#                         sheet.write(prod_row, prod_col + 4, each['cost_price'], font_size_8)
                        prod_row = prod_row + 1
#                 headertable(prod_row+2)
                prod_row = prod_row +6
#                 break
            break
        prod_row = 6
        prod_col = 4
        ro_inc = 0
        
        avail1=[]
        
        purvalue1=[]
        prodct1=[]
        adjt1=[]
        iq1=[]
        sq1=[]
        
        tq1=[]
        trfs1=[]
        
        for i in get_warehouse[1]:
            get_line = self.get_lines(data, i)
#             if not get_line:
#                 get_line = self.parentline(data, i)
            
            
            rem_dup = set()
            for ech in get_line:
                if ech['category'] not in rem_dup:
                    rem_dup.add(ech['category'])
                else:
                    pass
            
            for uniq in rem_dup:
                avail=[]
                
                purvalue=[]
                prodct=[]
                adjt=[]
                iq=[]
                sq=[]
               
                tq=[]
                trfs=[]
                
                
                if(ro_inc > 0):
                    prod_row = prod_row +6
#                     sheet.merge_range(prod_row+2, prod_col-2,prod_row+2, prod_col-1, 'Grand Total', font_size_8)
                      
                for each in get_line:
                    
                    if each['category'] == uniq:  
#                          opening
                        sheet.merge_range(prod_row+2, prod_col-2,prod_row+2, prod_col-1, 'Sub Total', formatblack)
                        if(data['form']['check'] == True):
                            if each['ob'] < 0:
                                sheet.merge_range(prod_row+1, prod_col,prod_row+1,prod_col+1, '{0:,.2f}'.format(each['ob']), red_mark)
                                avail.append(each['ob'])
                                avail1.append(each['ob'])
                                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1, '{0:,.2f}'.format(sum(avail)), font_size_8)
                            else:
                                avail.append(each['ob'])
                                avail1.append(each['ob'])
                                sheet.merge_range(prod_row+1, prod_col,prod_row+1,prod_col+1, '{0:,.2f}'.format(each['ob']), font_size_8)
                                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1, '{0:,.2f}'.format(sum(avail)), font_size_8)
    #                        Total
                            if each['purchase_value'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 2,prod_row+1, prod_col + 3, '{0:,.2f}'.format(each['purchase_value']), red_mark)
                                purvalue.append(each['purchase_value'])
                                purvalue1.append(each['purchase_value'])
                                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3, '{0:,.2f}'.format(sum(purvalue)), font_size_8)
                        
                            else:
                                sheet.merge_range(prod_row+1, prod_col + 2,prod_row+1, prod_col + 3, '{0:,.2f}'.format(each['purchase_value']), font_size_8)
                                purvalue.append(each['purchase_value'])
                                purvalue1.append(each['purchase_value'])
                                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3, '{0:,.2f}'.format(sum(purvalue)), font_size_8)
                        
                            
                            if each['production'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 4,prod_row+1, prod_col + 5, '{0:,.2f}'.format(each['production']), red_mark)
                                prodct.append(each['production'])
                                prodct1.append(each['production'])
                                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5, '{0:,.2f}'.format(sum(prodct)), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+4, prod_row+1, prod_col + 5,'{0:,.2f}'.format(each['production']), font_size_8)
                                prodct.append(each['production'])
                                prodct1.append(each['production'])
                                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5, '{0:,.2f}'.format(sum(prodct)), font_size_8)
                         
                            if each['transfers'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 6,prod_row+1, prod_col + 7,'{0:,.2f}'.format(each['transfers']), red_mark)
                                trfs.append(each['transfers'])
                                trfs1.append(each['transfers'])
                                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7, '{0:,.2f}'.format(sum(trfs)), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+6, prod_row+1, prod_col + 7,'{0:,.2f}'.format(each['transfers']), font_size_8)
                                trfs.append(each['transfers'])
                                trfs1.append(each['transfers'])
                                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7,'{0:,.2f}'.format(sum(trfs)), font_size_8) 
                             
                            if each['adjustment'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 8,prod_row+1, prod_col + 9,'{0:,.2f}'.format(each['adjustment']), red_mark)
                                adjt.append(each['adjustment'])
                                adjt1.append(each['adjustment'])
                                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9,'{0:,.2f}'.format(sum(adjt)), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+8, prod_row+1, prod_col + 9,'{0:,.2f}'.format(each['adjustment']), font_size_8)
                                adjt.append(each['adjustment'])
                                adjt1.append(each['adjustment'])
                                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9,'{0:,.2f}'.format(sum(adjt)), font_size_8)
                                                
                          
                            if each['issue_sale'] < 0:
                                iq.append(each['issue_sale'])
                                iq1.append(each['issue_sale'])
                                sheet.merge_range(prod_row+1,prod_col+10,prod_row+1,prod_col + 11,'{0:,.2f}'.format(each['issue_sale']), red_mark)
                                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11,'{0:,.2f}'.format(sum(iq)), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1,prod_col+10,prod_row+1,prod_col +11,'{0:,.2f}'.format(each['issue_sale']), font_size_8)
                                iq.append(each['issue_sale'])
                                iq1.append(each['issue_sale'])
                                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11,'{0:,.2f}'.format(sum(iq)), font_size_8)
                         
     
    #                         #for sale qty     
                            if each['sale_value'] < 0:
                                sq.append(each['sale_value'])
                                sq1.append(each['sale_value'])
                                sheet.merge_range(prod_row+1,prod_col+12,prod_row+1,prod_col + 13,'{0:,.2f}'.format(each['sale_value']), red_mark)
                                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13,'{0:,.2f}'.format(sum(sq)), font_size_8)
                         
                            else:
                                sq.append(each['sale_value'])
                                sq1.append(each['sale_value'])
                                sheet.merge_range(prod_row+1,prod_col+12,prod_row+1,prod_col + 13,'{0:,.2f}'.format(each['sale_value']), font_size_8)
                                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13,'{0:,.2f}'.format(sum(sq)), font_size_8)
                        
                            if each['cb'] < 0:
                                tq.append(each['cb'])
                                tq1.append(each['cb'])
                                sheet.merge_range(prod_row+1, prod_col+14,prod_row+1, prod_col+ 15,'{0:,.2f}'.format(each['cb']), red_mark)
                                sheet.merge_range(prod_row+2, prod_col+14,prod_row+2, prod_col+15,'{0:,.2f}'.format(sum(tq)), font_size_8)
                            
                            else:
                                tq.append(each['cb'])
                                tq1.append(each['cb'])
                                sheet.merge_range(prod_row+1, prod_col + 14,prod_row+1, prod_col+  15, '{0:,.2f}'.format(each['cb']), font_size_8)
                                sheet.merge_range(prod_row+2, prod_col+ 14,prod_row+2, prod_col+ 15, '{0:,.2f}'.format(sum(tq)), font_size_8)
                        else:
                            if each['ob'] < 0:
                                sheet.merge_range(prod_row+1, prod_col,prod_row+1,prod_col+1, each['ob'], red_mark)
                                avail.append(each['ob'])
                                avail1.append(each['ob'])
                                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1, sum(avail), font_size_8)
                            else:
                                avail.append(each['ob'])
                                avail1.append(each['ob'])
                                sheet.merge_range(prod_row+1, prod_col,prod_row+1,prod_col+1, each['ob'], font_size_8)
                                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1,sum(avail), font_size_8)
    #                        Total
                            if each['purchase_value'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 2,prod_row+1, prod_col + 3, each['purchase_value'], red_mark)
                                purvalue.append(each['purchase_value'])
                                purvalue1.append(each['purchase_value'])
                                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3, sum(purvalue), font_size_8)
                        
                            else:
                                sheet.merge_range(prod_row+1, prod_col + 2,prod_row+1, prod_col + 3,each['purchase_value'], font_size_8)
                                purvalue.append(each['purchase_value'])
                                purvalue1.append(each['purchase_value'])
                                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3,sum(purvalue), font_size_8)
                        
                            
                            if each['production'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 4,prod_row+1, prod_col + 5, each['production'], red_mark)
                                prodct.append(each['production'])
                                prodct1.append(each['production'])
                                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5,sum(prodct), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+4, prod_row+1, prod_col + 5,each['production'], font_size_8)
                                prodct.append(each['production'])
                                prodct1.append(each['production'])
                                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5,sum(prodct), font_size_8)
                         
                            if each['transfers'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 6,prod_row+1, prod_col + 7, each['transfers'], red_mark)
                                trfs.append(each['transfers'])
                                trfs1.append(each['transfers'])
                                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7,sum(trfs), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+6, prod_row+1, prod_col + 7,each['transfers'], font_size_8)
                                trfs.append(each['transfers'])
                                trfs1.append(each['transfers'])
                                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7,sum(trfs), font_size_8) 
                             
                            if each['adjustment'] < 0:
                                sheet.merge_range(prod_row+1, prod_col + 8,prod_row+1, prod_col + 9,  each['adjustment'], red_mark)
                                adjt.append(each['adjustment'])
                                adjt1.append(each['adjustment'])
                                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9, sum(adjt), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1, prod_col+8, prod_row+1, prod_col + 9,each['adjustment'], font_size_8)
                                adjt.append(each['adjustment'])
                                adjt1.append(each['adjustment'])
                                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9, sum(adjt), font_size_8)
                                                
                          
                            if each['issue_sale'] < 0:
                                iq.append(each['issue_sale'])
                                iq1.append(each['issue_sale'])
                                sheet.merge_range(prod_row+1,prod_col+10,prod_row+1,prod_col + 11, each['issue_sale'], red_mark)
                                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11, sum(iq), font_size_8)
                         
                            else:
                                sheet.merge_range(prod_row+1,prod_col+10,prod_row+1,prod_col +11,each['issue_sale'], font_size_8)
                                iq.append(each['issue_sale'])
                                iq1.append(each['issue_sale'])
                                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11,sum(iq), font_size_8)
                         
     
    #                         #for sale qty     
                            if each['sale_value'] < 0:
                                sq.append(each['sale_value'])
                                sq1.append(each['sale_value'])
                                sheet.merge_range(prod_row+1,prod_col+12,prod_row+1,prod_col + 13, each['sale_value'], red_mark)
                                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13, sum(sq), font_size_8)
                         
                            else:
                                sq.append(each['sale_value'])
                                sq1.append(each['sale_value'])
                                sheet.merge_range(prod_row+1,prod_col+12,prod_row+1,prod_col + 13,each['sale_value'], font_size_8)
                                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13, sum(sq), font_size_8)
                        
                            if each['cb'] < 0:
                                tq.append(each['cb'])
                                tq1.append(each['cb'])
                                sheet.merge_range(prod_row+1, prod_col+14,prod_row+1, prod_col+ 15, each['cb'], red_mark)
                                sheet.merge_range(prod_row+2, prod_col+14,prod_row+2, prod_col+15, sum(tq), font_size_8)
                            
                            else:
                                tq.append(each['cb'])
                                tq1.append(each['cb'])
                                sheet.merge_range(prod_row+1, prod_col + 14,prod_row+1, prod_col+  15, each['cb'], font_size_8)
                                sheet.merge_range(prod_row+2, prod_col+ 14,prod_row+2, prod_col+ 15,sum(tq), font_size_8)
#                             sheet.merge_range(prod_row+2, prod_col+p_col_inc + 8,prod_row+2, prod_col+p_col_inc + 9, sum(cb), font_size_8)
                        prod_row = prod_row + 1
                    ro_inc=ro_inc+1
            
#                     footertable(prod_row+1)
            if(data['form']['check'] == True):
                sheet.merge_range(prod_row+2, prod_col-2,prod_row+2, prod_col-1, 'Grand Total', formatblack)
                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1, '{0:,.2f}'.format(sum(avail1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3, '{0:,.2f}'.format(sum(purvalue1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5, '{0:,.2f}'.format(sum(prodct1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7, '{0:,.2f}'.format(sum(trfs1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9, '{0:,.2f}'.format(sum(adjt1)), font_size_8) 
                
                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11, '{0:,.2f}'.format(sum(iq1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13,'{0:,.2f}'.format( sum(sq1)), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+14,prod_row+2, prod_col+15, '{0:,.2f}'.format(sum(tq1)), font_size_8)
              
            else:
                sheet.merge_range(prod_row+2, prod_col-2,prod_row+2, prod_col-1, 'Grand Total', formatblack)
                sheet.merge_range(prod_row+2, prod_col,prod_row+2, prod_col+1, sum(avail1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+2,prod_row+2, prod_col+3, sum(purvalue1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+4,prod_row+2, prod_col+5, sum(prodct1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+6,prod_row+2, prod_col+7, sum(trfs1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+8,prod_row+2, prod_col+9, sum(adjt1), font_size_8) 
                
                sheet.merge_range(prod_row+2, prod_col+10,prod_row+2, prod_col+11, sum(iq1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+12,prod_row+2, prod_col+13, sum(sq1), font_size_8)
                sheet.merge_range(prod_row+2, prod_col+14,prod_row+2, prod_col+15, sum(tq1), font_size_8)
              
                   
            prod_row = 5
#             prod_row = prod_row +3
            prod_col = prod_col + 11
