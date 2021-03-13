# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar


class GatepassReportReport(models.Model):
    _name = "gatepass.report.wizard"
    _description = "Employee Wizard"

    date_from = fields.Date(string="Date From", default=datetime.datetime.today())
    date_to = fields.Date(string="Date To", default=datetime.datetime.today())
    # total = fields.Char(string="Totall")

    # delivery = fields.Many2one('stock.picking', string="Delivery")
