from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PayrollPayemntWizard(models.TransientModel):
    _name = 'payroll.payment.wizard'
    _description = 'Payroll Payment'

    journal_id = fields.Many2one('account.journal', string="Journal")
    payment_date = fields.Date(string="Payment Date")
    payslip_lines = fields.Many2many('hr.payslip')

    def create_data(self):
#         model = self.env.context.get('active_model')
#         rec = self.env[model].browse(self.env.context.get('active_id'))
        for record in self.payslip_lines:
            rec = self.env['account.account'].search([('user_type_id','=', 'Payable')])[0]
#         raise UserError(_(rec.id))
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
            for oline in self.payslip_lines:
                debit_line = (0, 0, {
                    'name': oline.number,
                    'debit': abs(oline.net_wage),
                    'credit': 0.0,
                    'partner_id': oline.employee_id.id,
                    # 'analytic_account_id': oline.analytic_account_id.id,
                    # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                    'account_id': rec.id,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                credit_line = (0, 0, {
                    'name': oline.number,
                    'debit': 0.0,
                    'partner_id': oline.employee_id.id,
                    'credit': abs(oline.net_wage),
                    'account_id': rec.id,
                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            move_dict['line_ids'] = line_ids
            move = record.env['account.move'].create(move_dict)
            print("General entry created")
        
        
    def general_entry(self):
#         raise UserError(_('Error'))
        rec = self.env['account.account'].search([('user_type_id','=', 'Payable')])[0]
#         raise UserError(_(rec.id))
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        move_dict = {
            'name': self.payslip_lines.number,
            'journal_id': self.journal_id.id,
            'partner_id': self.payslip_lines.employee_id.id,
            'date': self.payment_date,
            'state': 'draft',
        }
        for oline in self.payslip_lines:
            debit_line = (0, 0, {
                'name': oline.number,
                'debit': abs(oline.net_wage),
                'credit': 0.0,
                'partner_id': oline.employee_id.id,
                # 'analytic_account_id': oline.analytic_account_id.id,
                # 'analytic_tag_ids': [(6, 0, oline.analytic_tag_ids.ids)],
                'account_id': rec.id,
            })
            line_ids.append(debit_line)
            debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            credit_line = (0, 0, {
                'name': oline.number,
                'debit': 0.0,
                'partner_id': oline.employee_id.id,
                'credit': abs(oline.net_wage),
                'account_id': rec.id,
            })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)
        print("General entry created")
        