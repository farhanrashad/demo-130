# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import api, fields, models, _

class InvoiceOutstanding(models.TransientModel):
    _name = "sale.register"
    _description = "Sale Register model"

    start_date = fields.Date(string='From Date', required='1', help='select start date')
    end_date = fields.Date(string='To Date', required='1', help='select end date')
    total_quantity_due = fields.Integer(string='Total quantity Amount')
    total_amount_due = fields.Integer(string='Total credit Amount')
    total_tax_due = fields.Integer(string='Total tax Amount')



    def check_report(self):
        data = {}
        data['form'] = self.read(['start_date', 'end_date'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date', 'end_date'])[0])
        return self.env.ref('de_account_invoice_register.action_sale_invoice_register').report_action(self, data=data, config=False)


