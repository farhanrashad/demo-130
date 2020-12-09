from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class PayrollPaymentWizard(models.TransientModel):
    _name = 'payroll.payment.wizard'
    _description = 'Payroll Payment'

    journal_id = fields.Many2one('account.journal', string="Journal")
    payment_date = fields.Date(string="Payment Date", compute='get_date')
    payslip_lines = fields.Many2many('hr.payslip')
    payslip_line = fields.One2many('payroll.payment.wizard.line', 'payment_id')
    is_lines_added = fields.Boolean('Is Lines Added?', default=False)

    @api.onchange('payment_date')
    def get_date(self):
        self.payment_date = datetime.today().date()

    @api.onchange('payment_date')
    def get_lines(self):
        if self.is_lines_added == False:
            for rec in self.payslip_lines:
                record = self.env['payroll.payment.wizard.line'].create({
                    'payment_id': self.id,
                    'name': rec.name,
                    'journal_id': rec.journal_id.id,
                    'employee_id': rec.employee_id.id,
                    'number': rec.number,
                    'net_wage': rec.net_wage,
                })
            self.is_lines_added = True

    def create_data(self):
        for record in self.payslip_line:
            rec = self.env['account.account'].search([('user_type_id', '=', 'Payable')])
            if len(rec) > 0:
                rec = rec[0]
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                move_dict = {
                    'name': record.number,
                    'journal_id': self.journal_id.id,
                    'partner_id': record.employee_id.id,
                    'date': self.payment_date,
                    'state': 'draft',
                }
                for oline in self.payslip_line:
                    if oline.amount_to_pay < oline.net_wage:
                        amount = 0
                        amount = oline.amount_to_pay if oline.amount_to_pay > 0 else oline.net_wage
                        debit_line = (0, 0, {
                            'name': oline.number,
                            'debit': amount,
                            'credit': 0.0,
                            'partner_id': oline.employee_id.id,
                            'account_id': rec.id,
                        })
                        line_ids.append(debit_line)
                        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                        credit_line = (0, 0, {
                            'name': oline.number,
                            'debit': 0.0,
                            'partner_id': oline.employee_id.id,
                            'credit': amount,
                            'account_id': rec.id,
                        })
                        line_ids.append(credit_line)
                        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
                    else:
                        raise ValidationError(_("Amount to Pay is Greater than Due Amount!!!!!"))

                move_dict['line_ids'] = line_ids
                move = record.env['account.move'].create(move_dict)
                print("General entry created")
            else:
                raise ValidationError(_("There is no Payable Account."))


class PayrollPaymentWizardLine(models.TransientModel):
    _name = 'payroll.payment.wizard.line'
    _description = 'Payroll Payment Line'

    payment_id = fields.Many2one('payroll.payment.wizard')
    employee_id = fields.Many2one('hr.employee')
    number = fields.Char('Number')
    name = fields.Char('Name')
    journal_id = fields.Many2one('account.journal')
    net_wage = fields.Float('Due Amount')
    amount_to_pay = fields.Float('Amount To Pay')
