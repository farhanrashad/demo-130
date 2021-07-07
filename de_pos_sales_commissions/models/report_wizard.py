from datetime import datetime
from dateutil import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PrintCommissionSummaryReport(models.TransientModel):
    _name = 'commission.report' 
    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    user = fields.Many2one(comodel_name='res.users', string='User')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Employee', required=True)
    session_id = fields.Many2one(comodel_name='pos.config', string='Outlet')
    status = fields.Selection([
        ('paid', 'Paid'),
        ('draft', 'Draft')],
        string='Status')

    def generate_report(self):
        active_ids = self.env.context.get('active_ids', [])
        data = {
            'ids': active_ids,
            'model': 'report.model',
            'form': self.read()[0]
        }
        return self.env.ref('de_pos_sales_commissions.report_commission_summary_detail').report_action(self, data=data)


class CommissionSummaryReport(models.AbstractModel):
    _name = 'report.de_pos_sales_commissions.report_custom_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_('Form content is missing, this report cannot be printed.'))
        outlet_id = ''
        if data['form']['session_id']:
            outlet_id = self.env['pos.config'].search([('id', '=', data['form']['session_id'][0])])
        vals = []
        lval = []
        user = []
        if(data['form']['start_date'] != False and data['form']['end_date'] != False and data['form']['employee_id'] != False):
            print('data', data['form']['employee_id'][1])
            com = self.env['commission.form'].search([
                ('employee_id', '=', data['form']['employee_id'][1]),
                ('order_date', '>=', data['form']['start_date']),
                ('order_date', '<=', data['form']['end_date'])
            ])
            for y in com:
                vals.append(y)
            # lval.append(('User', '=', data['form']['user'][1]))
            if data['form']['start_date']:
                lval.append(('order_date', '>=', data['form']['start_date']))
            if data['form']['end_date']:
                lval.append(('order_date', '<=', data['form']['end_date']))
            if data['form']['session_id']:
                lval.append(('config_id', '=', data['form']['session_id'][0]))
        idvs = []
        for i in vals:
            idvs.append(i.id)
        single = list(set(vals))
        vr = []
        for vl in single:
            for v in vl:
                vr.append(v.id)
        single2 = list(set(vr))       
        lval.append(('id', 'in', single2))
        in_cr = self.env['commission.form'].search(lval)
        return {
            'datacr': in_cr,
            'date_order': data['form']['start_date'],
            'date_order2': data['form']['end_date'],
            'users': data['form']['employee_id']
        }
