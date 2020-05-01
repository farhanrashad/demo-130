from odoo import models


class OrderjobXlsx(models.AbstractModel):
    _name = 'report.de_construction_app.order_job_xlx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # format1 = workbook.add_format({'font-size': 14, 'align': 'vcenter', 'bold': True})
        # format2 = workbook.add_format({'font-size':10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Invoicing record')
        sheet.write(1, 2, 'Name')
        sheet.write(1, 4, 'Assign to')
        sheet.write(1, 6, 'Starting Date')
        sheet.write(1, 8, 'Ending Date')
        sheet.write(1, 10, 'Customer Name')
        sheet.write(2, 2, lines.name)
        # sheet.write(2, 4, lines.assign_to)
        # sheet.write(2, 4, lines.tags)
        sheet.write(2, 6, lines.starting_date)
        sheet.write(2, 8, lines.ending_date)
        # sheet.write(2, 10, lines.customer_name)
        # sheet.write(2, 12, lines.customer_name)

