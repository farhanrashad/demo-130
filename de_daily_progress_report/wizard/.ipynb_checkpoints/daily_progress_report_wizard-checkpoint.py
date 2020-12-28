# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class ProgressReportWizard(models.TransientModel):
    _name = 'progress.report.wizard'

    date = fields.Date(string="Set Date")

    def progress_report(self):
        pass
#         data = {}
#         data['form'] = self.read(['date_from', 'date_to','lot_number_from','lot_number_to'])[0]
#         return self._print_report(data)

#     def _print_report(self, data):
#         print('_print_report\n')
#         data['form'].update(self.read(['date_from', 'date_to','lot_number_from','lot_number_to'])[0])
#         return self.env.ref('de_daily_progress_report.lot_get_report_id').with_context(landscape=True).report_action(
#             self, data=data, config=False)