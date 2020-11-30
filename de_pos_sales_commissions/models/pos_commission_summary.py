from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PosCommissionSummary(models.Model):
    _name = 'commission.summary'
    _description = 'Create commission summary'

    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    all_user = fields.Boolean('All Employees')
    #     user = fields.Many2many('res.users', string="User(s)")
    user = fields.Many2many('hr.employee', string="Employee(s)")

    @api.onchange('all_user')
    def user_auto(self):
        if not self.all_user == True:
            self.user = None
        if self.all_user == True:
            employee = self.env['hr.employee'].search([])
            self.user = employee

    def create_invoice(self):
        for order in self:
            invoice_line_ids = []
            if (order.start_date and order.end_date):
                invoice_line = []
                data_list = []

                account = self.env['account.account'].search([('name', '=', 'POSCommission')])
                employee_ids = self.env['hr.employee'].search([('id', 'in', order.user.ids)])
                for employee in employee_ids:
                    total_commission = 0

                    commission_data = self.env['commission.form'].search(
                        [('order_date', '>=', order.start_date), ('order_date', '<=', order.end_date),
                         ('active_employee', '=', employee.id), ('state', '=', 'done')])

                    if not commission_data:
                        raise UserError((
                                'No Record found against applied user: ' + employee.name + '\nKindly deselect all records not in done stage.'))
                    for data in commission_data:
                        if not data.active_employee.address_home_id:
                            raise UserError(
                                ('Partner of employee is not linked: ' + data.active_employee.name))

                        total_commission = total_commission + data.commission_amount
                        data.state = 'billed'

                    inv_obj = {
                        'partner_id': data.active_employee.address_home_id.id,
                        'invoice_date': fields.Date.today(),
                        'type': 'in_invoice',
                        'name': '/',
                        'state': 'draft',
                        'invoice_line_ids': [(0, 0, {'name': data.source_document,
                                                     'account_id': account.id,
                                                     'quantity': 1.0,
                                                     'price_unit': total_commission, })],
                    }

                    record = self.env['account.move'].create(inv_obj)