# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PayrollPayment(models.Model):
    _inherit = 'hr.payslip'

        
    def action_payslip_payment_wizard(self):
        payslip_list = []
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['hr.payslip'].browse(selected_ids)
            
            for record in selected_records:
                payslip_list.append(record.id)
        return {
                'type': 'ir.actions.act_window',
                'name': 'Payroll Payment',
                'view_id':self.env.ref('de_payroll_payment.view_payroll_payment_wizard_form', False).id,
                'target': 'new',
                'context': {'default_payslip_lines': payslip_list},
                'res_model': 'payroll.payment.wizard',
                'view_mode': 'form',
            }
    
    def action_journal_entries(self):
        tree_view_id = self.env.ref('account.view_move_tree').ids
        form_view_id = self.env.ref('account.view_move_form').ids
        return {
            'name': _('Journal Entries'),
            'view_mode': 'tree',
            'res_model': 'account.move',
            'views': [[tree_view_id, 'tree'], [form_view_id, 'form']],
            # 'view_id': self.env.ref('account.view_move_tree', False).id,
            'type': 'ir.actions.act_window',
            'domain': [('name', '=', self.number)],
        }
