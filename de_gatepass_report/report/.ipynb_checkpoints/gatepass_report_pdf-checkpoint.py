# -*- coding: utf-8 -*-

from odoo import api, models
from dateutil.parser import parse
from datetime import datetime
from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar


class GatepassReportPdf(models.AbstractModel):
    _name = 'report.de_gatepass_report.gatepass_report_print'
    def get_gatepass(self, employee_id, date):
        
        
        
        
    def _get_report_values(self, docids, data=None):
        
        
        return {
            'doc_ids': self.ids,
            'doc_model': 'hr_attendance.hr.attendance',
            'get_gatepass': self.get_gatepass,
        }