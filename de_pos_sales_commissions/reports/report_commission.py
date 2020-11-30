from datetime import datetime
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class print_commission_summary_report(models.TransientModel):
    _name = 'commission.report'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    user = fields.Many2one('hr.employee', string="Employee", required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('billed', 'Billed'),
    ], store=True, default='draft')

    def generate_report(self):
        active_ids = self.env.context.get('active_ids', [])
        datas = {
            'ids': active_ids,
            'model': 'report.model',
            'form': self.read()[0]
        }
        return self.env.ref('de_pos_sales_commissions.report_commission_summary_detail').report_action(self, data=datas)


class commission_summary_report(models.AbstractModel):
    _name = 'report.de_pos_sales_commissions.report_custom_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        vals = []
        lval = []

        if (data['form']['start_date'] != False and data['form']['end_date'] != False and data['form'][
            'user'] != False):
            commission_details = self.env['commission.form'].search([
                ('active_employee', '=', data['form']['user'][1]),
                ('order_date', '>=', data['form']['start_date']),
                ('order_date', '<=', data['form']['end_date']),
                ('state', '=', data['form']['status']),
            ])
            if not commission_details:
                raise UserError(('No record found against applied employee!'))

            for y in commission_details:
                vals.append(y)

            lval.append(('active_employee', '=', data['form']['user'][1]))
            lval.append(('order_date', '>=', data['form']['start_date']))
            lval.append(('order_date', '<=', data['form']['end_date']))
        #             lval.append(('state','=',data['form']['status'])

        idvs = []
        # testing
        for i in vals:
            idvs.append(i.id)
        # testing
        single = list(set(vals))
        vr = []
        for vl in single:
            for v in vl:
                vr.append(v.id)

        single2 = list(set(vr))
        lval.append(('id', 'in', single2))
        in_cr = self.env['pos.commission'].search(lval)

        return {
            'datacr': in_cr,
            'date_order': data['form']['start_date'],
            'date_order2': data['form']['end_date'],
            'users': data['form']['user']
        }