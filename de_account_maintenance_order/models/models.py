# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MaintenanceOrder(models.Model):
    _inherit = 'stock.move'
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True,)
    account_id = fields.Many2one(related='em_order_id.account_id')
    price_unit = fields.Float(related='product_id.lst_price')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account',
        readonly=True, copy=False, check_company=True,  # Unrequired company
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="The analytic account related to a sales order.")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.company.currency_id.id)
   

    
    @api.depends('price_subtotal','price_unit')    
    def _compute_amount(self):
        self.ensure_one()
        self.price_subtotal = self.price_unit * self.product_uom_qty
#             t = line.price_unit
#             p = line.product_uom_qty
#             line.update({
#                 'price_subtotal': line.price_unit * line.product_uom_qty
                
#             })

   
    class MaintenanceOrder(models.Model):
        _inherit = 'maintenance.order'
        
        debit_account_id = fields.Many2one('account.account', string='Account')
        account_id = fields.Many2one('account.account', string='Account')
        credit_account_id = fields.Many2one('account.account', string='Account')
        journal_id = fields.Many2one('account.journal', string='Journal')
        
        def _action_start_maintenance(self):
            debit_vals = {
                  'name': self.name,
                  'debit': abs(self.move_lines.price_subtotal),
                  'credit': 0.0,
                  'account_id': self.debit_account_id.id,
                  'tax_line_id': adjustment_type == 'debit' and self.tax_id.id or False,
                     }
            credit_vals = {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.move_lines.price_subtotal),
                  'account_id': self.credit_account_id.id,
                  'tax_line_id': adjustment_type == 'credit' and self.tax_id.id or False,
                  }
            vals = {
                  'journal_id': self.journal_id.id,
                  'date': self.date,
                  'state': 'draft',
                  'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                   }
            move = self.env['account.move'].create(vals)
            result = super(MaintenanceOrder, self)._action_start_maintenance()
            return result

        
#         def _action_start_maintenance(self):
#             vals = {
#             'ref': self.name,
#             'date': self.date_order,
#             'journal_id': self.journal_id.id,
#             # 'stock_move_id': self.stock_move_id,
#             'company_id': self.move_lines.company_id.id,
#             }
#             picking = self.env['account.move'].create(vals)
#             for line in self.move_lines:
#                 lines = {
#                   'move_id': picking.id,
#                   'product_id': line.product_id.id,
#                   'account_id': self.account_id.id,
# #                   'partner_id': line.product_id.uom_id.id,
#                   'debit': 5,
#                   'credit': 5,
#                 # 'bom_id': line.bom_id.id,
#                 'product_uom_qty': line.product_uom_qty,
# #                 'quantity_done': line.transfer_in_quantity,
#             }
#             stock_move = self.env['account.move.line'].create(lines)
#             result = super(MaintenanceOrder, self)._action_start_maintenance()
#             return result