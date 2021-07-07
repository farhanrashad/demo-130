# -*- coding: utf-8 -*-
import base64
from datetime import datetime
from io import BytesIO
import calendar
from calendar import monthrange

from flectra import models, fields, api, _
from flectra.tools.misc import xlwt


class EmpLocation(models.Model):
    _name = 'emp.location'

    name = fields.Char("Location")


class PessiLocation(models.Model):
    _name = 'pessi.location'

    name = fields.Char("Location")


class HrEmployeeExt(models.Model):
    _inherit = "hr.employee"

    emp_location = fields.Many2one('emp.location', 'Work Location')
    pessi_location = fields.Many2one('pessi.location', 'Pessi Location')
    emp_status = fields.Selection([('contract', 'Contract'), ('permanent', 'Permanent')], string='Status')
    eobi_status = fields.Selection([('SubCode', 'SubCode'), ('MainCode', 'MainCode')], string='Status for EOBI')
    nature_of_work = fields.Selection([('skilled', 'Skilled'), ('nonskilled', 'Non Skilled')], string='Nature of Work')
    eobi_no = fields.Char(string ='EOBI NO')


class wizard_excel_report(models.TransientModel):
    _name = "hr.contributation.register.wizard"

    pessi_location = fields.Many2many('pessi.location',
                                    string='Pessi Location',
                                    required=True
                                    )
    excel_file = fields.Binary('excel file')
    file_name = fields.Char('Excel File', size=64)
    inventory_printed = fields.Boolean('Payment Report Printed')

    @api.model
    def _get_year_init(self):
        today_str = fields.Date.context_today(self)
        today = fields.Date.from_string(today_str)
        return today.replace(day=1, month=1)

    date_from = fields.Date(
        string='Date from',
        default=_get_year_init,
        required=True)
    date_to = fields.Date(
        string='Date to',
        default=fields.Date.context_today, required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Work Address')
    branch_id = fields.Many2one(comodel_name='res.branch', string='Branch')

    @api.multi
    def pessi_report(self):
        active_ids = self.env.context.get('active_ids', []) or []
        record = self.env['hr.contribution.register'].browse(active_ids)

        workbook = xlwt.Workbook()
        column_heading_style = xlwt.easyxf('font:height 200;font:bold True;')
        count = 15
        row = 3
        sr_number = 0
        loop = 4
        total_gross = 0.0
        total_net = 0.0
        total_pessi = 0.0
        rate_per_day = 0
        per_day_count = 0.0
        row_count = 0
        worksheet = workbook.add_sheet('ws1',cell_overwrite_ok=True)
        style_so = xlwt.easyxf(
            'font:bold on; align: wrap on, horiz center; align: vert centre; font:height 250; pattern: pattern solid, fore_colour white;  border: top thin, right thin, bottom thin, left thin;')
        columns_center_bold_style_with_border = xlwt.easyxf(
            'font:height 220; align: wrap on, horiz center; font: bold on;pattern: pattern solid, fore_colour light_yellow;  border: top thin, right thin, bottom thin, left thin;')
        worksheet.row(0).height = 900
        worksheet.row(1).height = 400
        worksheet.row(2).height = 400
        worksheet.row(3).height = 600
        worksheet.col(0).width = 3000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 4000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 6500
        worksheet.col(5).width = 4000
        worksheet.col(6).width = 3000
        worksheet.col(7).width = 4500
        worksheet.col(8).width = 5000
        worksheet.col(9).width = 4000
        worksheet.col(10).width = 3000
        worksheet.col(11).width = 6000
        worksheet.col(12).width = 8000
        # worksheet.row(0).height = 500

        report_head = "Punjab Employee's Social Security Institute- 26 Main Gulberg, Lahore"
        worksheet.write_merge(0, 0, 4, 5, report_head, style_so)
        date_format = "%Y-%m-%d"
        a = datetime.strptime(self.date_from, date_format)
        worksheet.write(1, 4, 'FROM', columns_center_bold_style_with_border)
        worksheet.write(1, 5, self.date_from, columns_center_bold_style_with_border)
        worksheet.write(2, 4, 'TO', columns_center_bold_style_with_border)
        worksheet.write(2, 5, self.date_to, columns_center_bold_style_with_border)
        worksheet.write(row, 0, 'SR. No.', columns_center_bold_style_with_border)
        worksheet.write(row, 1, 'NAME', columns_center_bold_style_with_border)
        worksheet.write(row, 2, 'CODE', columns_center_bold_style_with_border)
        worksheet.write(row, 3, 'CNIC', columns_center_bold_style_with_border)
        worksheet.write(row, 4, 'DESIGNATION', columns_center_bold_style_with_border)
        worksheet.write(row, 5, 'Date of joining', columns_center_bold_style_with_border)
        worksheet.write(row, 6, 'No of Days', columns_center_bold_style_with_border)
        worksheet.write(row, 7, 'Nature of Employment', columns_center_bold_style_with_border)
        worksheet.write(row, 8, 'Gross Salary', columns_center_bold_style_with_border)
        worksheet.write(row, 9, 'Rate Per Day', columns_center_bold_style_with_border)
        worksheet.write(row, 10, 'Net Salary', columns_center_bold_style_with_border)
        worksheet.write(row, 11, 'PESSI Contribution Payable', columns_center_bold_style_with_border)
        worksheet.write(row, 12, 'Location', columns_center_bold_style_with_border)
        to_date = datetime.strptime(self.date_to, '%Y-%m-%d')
        todate_year = int(self.date_to.split('-')[0])
        todate_month = int(self.date_to.split('-')[1])
        nod = monthrange(todate_year, todate_month)[1]
        between_date = self.env['hr.payslip.run'].search(
            [('date_start', '>=', (self.date_from)), ('date_end', '<=', self.date_to)])
        # if len(between_date) > 1:
        for rec in between_date:

            for slip_ids in rec.slip_ids:
                row_count = row_count + 1
                worksheet.row(loop).height = 350
                emp_id = self.env['hr.employee'].search([('contact_branch_id', '=', self.branch_id.id)])
                if slip_ids.employee_id.id in emp_id.ids:
                    row += 1
                    sr_number += 1
                    worksheet.write(row, 0, sr_number)
                    worksheet.write(row, 1, slip_ids.employee_id.name)
                    worksheet.write(row, 2, slip_ids.employee_id.code)
                    worksheet.write(row, 3, slip_ids.employee_id.identification_id)
                    worksheet.write(row, 4, slip_ids.employee_id.job_id.name)
                    # worksheet.write(row, 5, slip_ids.employee_id.emp_status)
                    # worksheet.write(row, 6, slip_ids.employee_id.nature_of_work)
                    worksheet.write(row, 5, slip_ids.employee_id.joining_date)
                    # doj_year = int(slip_ids.employee_id.joining_date.split('-')[0])
                    # doj_month = int(slip_ids.employee_id.joining_date.split('-')[1])
                    # current_date = str(datetime.today())
                    # number_of_days = 0
                    # current_date.split('-')[1]
                    date_format = "%Y-%m-%d"
                    a = datetime.strptime(slip_ids.date_to, date_format)
                    b = datetime.strptime(slip_ids.date_from, date_format)

                    if slip_ids.employee_id.contract_id.date_start != False:
                        c = datetime.strptime(slip_ids.employee_id.contract_id.date_start, date_format)
                        # print("  ", a, "    ", b, "    ", c)
                        if (b.month == c.month and b.year == c.year):
                            delta = a - c
                            dayss = delta.days + 1
                            worksheet.write(row, 6, dayss)

                        else:
                            delta = a - b
                            dayss = delta.days + 1
                            worksheet.write(row, 6, dayss)

                    else:
                        delta = a - b
                        dayss = delta.days + 1
                        worksheet.write(row, 6, dayss)
                    for pessi in slip_ids.details_by_salary_rule_category:
                            if pessi.code == 'GROSS':
                                total_gross += pessi.total
                                worksheet.write(row, 8, pessi.total)
                    worksheet.write(row, 7, self.env['hr.contract'].search(
                        [('employee_id.id', '=', slip_ids.employee_id.id), ('state', '=', 'open')]).schedule_pay)
                    if self.env['hr.contract'].search([('employee_id.id', '=', slip_ids.employee_id.id), ('state', '=', 'open')]).pessi_amount:
                        rate_per_day = self.env['hr.contract'].search(
                            [('employee_id.id', '=', slip_ids.employee_id.id), ('state', '=', 'open')]).pessi_amount / 30
                        worksheet.write(row, 9, int(rate_per_day))
                        per_day_count = per_day_count + rate_per_day
                    else:
                        worksheet.write(row, 9, '0')
                    if self.env['hr.contract'].search(
                            [('employee_id.id', '=', slip_ids.employee_id.id), ('state', '=', 'open')]).pessi_amount:
                        net_salary = dayss * rate_per_day
                        total_net += net_salary
                        worksheet.write(row, 10, int(net_salary))
                    else:
                        worksheet.write(row, 10, '0')
                    for pessi in slip_ids.details_by_salary_rule_category:
                        if pessi.code == 'PESSI':
                            total_pessi += pessi.total
                            worksheet.write(row, 11, pessi.total)
                    worksheet.write(row, 12, self.branch_id.name)
                loop += 1
        # worksheet.row(loop - 63).height = 600
        print('loop', loop)
        print('count', row_count)
        print('no', sr_number)
        worksheet.write(sr_number+6, 6, 'Total :', columns_center_bold_style_with_border)
        worksheet.write(sr_number+6, 7, '###', columns_center_bold_style_with_border)
        worksheet.write(sr_number+6, 8, abs(total_gross), columns_center_bold_style_with_border)
        worksheet.write(sr_number + 6, 9, abs(per_day_count), columns_center_bold_style_with_border)
        worksheet.write(sr_number+6, 10, abs(total_net), columns_center_bold_style_with_border)
        worksheet.write(sr_number+6, 11, abs(total_pessi), columns_center_bold_style_with_border)
        print('per', per_day_count)
                    # if slip_ids.employee_id.joining_date.split('-')[0] == current_date.split('-')[0] and \
                    #         slip_ids.employee_id.joining_date.split('-')[1] == current_date.split('-')[1]:
                    #     number_of_days = monthrange(doj_year, doj_month)[1] - int(current_date.split('-')[2].split(' ')[0])
                    #     worksheet.write(row, 8, number_of_days)
                    # else:
                    #     number_of_days = monthrange(doj_year, doj_month)[1]
                    #     worksheet.write(row, 8, number_of_days)

                    # worksheet.write(row, 9, self.env['hr.contract'].search(
                    #     [('employee_id.id', '=', slip_ids.employee_id.id)]).schedule_pay)
                    # worksheet.write(row, 10, self.env['hr.contract'].search(
                    #     [('employee_id.id', '=', slip_ids.employee_id.id)]).pessi_amount)
                    # rate_per_day = 0
                    # if self.env['hr.contract'].search([('employee_id.id', '=', slip_ids.employee_id.id)]).pessi_amount:
                    #     rate_per_day = self.env['hr.contract'].search(
                    #         [('employee_id.id', '=', slip_ids.employee_id.id)]).pessi_amount / 30
                    #     worksheet.write(row, 11, int(rate_per_day))
                    # else:
                    #     worksheet.write(row, 11, '0')
                    #
                    # if self.env['hr.contract'].search(
                    #     [('employee_id.id', '=', slip_ids.employee_id.id)]).pessi_amount:
                    #     net_salary = dayss * rate_per_day
                    #     worksheet.write(row, 12, int(net_salary))
                    # else:
                    #     worksheet.write(row, 12, '0')
                    #
                    # for pessi in slip_ids.details_by_salary_rule_category:
                    #     if pessi.code == 'PESSI':
                    #         worksheet.write(row, 13, pessi.total)
                    #
                    #
                    # worksheet.write(row, 14, slip_ids.employee_id.pessi_location.name)




        fp = BytesIO()
        workbook.save(fp)
        self.file_name = 'PESSI Report.xls'
        inventory_printed = True

        record_id = self.env['hr.contributation.register.wizard'].create(
            {'excel_file': base64.encodestring(fp.getvalue()),
             'inventory_printed': True,
             'file_name': self.file_name}, )

        return {
            'view_mode': 'form',
            'res_id': record_id.id,
            'res_model': 'hr.contributation.register.wizard',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self.env.context,
            'target': 'new',
        }