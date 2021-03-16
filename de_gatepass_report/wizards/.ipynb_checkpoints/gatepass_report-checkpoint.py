# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar


class GatepassReportReport(models.TransientModel):
    _name = "gatepass.report.wizard"
    _description = "Employee Wizard"

    date_from = fields.Date(string="Date From", default=datetime.datetime.today())
    date_to = fields.Date(string="Date To", default=datetime.datetime.today())
    total_acc_qty = fields.Boolean(string="Total Accumulate Gatepass QTY")
    show_products = fields.Boolean(string="Show Only Full Sent Products")
    delivery_order = fields.Many2one('stock.picking', string="Delivery Order")
    
    
    
    
    
    def generate_pdf_report(self):
        
        data = {}
            
        return self.env.ref('de_gatepass_report.de_gatepass_report_id').report_action([], data=data)