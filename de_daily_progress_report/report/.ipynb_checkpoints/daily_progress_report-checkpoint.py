# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class ReportReceivingUtilize(models.AbstractModel):
    _name = 'report.de_daily_progress_report.progress_report_template'

    '''Find Purchase invoices between the date and find total outstanding amount'''
#     @api.model
#     def _get_report_values(self, docids, data=None):
#         print('_get_report_values\n')
#         self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_id'))
#         outstanding_invoice = []       
        
#         lot_records = self.env['stock.move.line'].search([('date', '>=', docs.date_from),
#                                                           ('date', '<=', docs.date_to),
#                                                           ('lot_id', '>=', docs.lot_number_from.id),
#                                                           ('lot_id', '<=', docs.lot_number_to.id),])


#         if lot_records:
        #    amount_due = 0
        #    for total_amount in invoices:
        #        amount_due += total_amount.amount_residual
        #    docs.total_amount_due = amount_due

#             return {
#                 'docs': docs,
#                 'lot_records': lot_records,
#             }
#         else:
#             raise UserError("There is not any Lot/Serial numbers between selected dates")

            
    
