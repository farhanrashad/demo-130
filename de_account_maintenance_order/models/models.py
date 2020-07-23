# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MaintenanceOrder(models.Model):
    _inherit = 'maintenance.order.line'
    
    @api.model
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Accounts Receivable'),],
            limit=1).id
    
    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True,)
    account_id = fields.Many2one('account.account', string='Account',
        index=True, ondelete="restrict", check_company=True,
        domain=[('deprecated', '=', False)],  default = _get_default_account )
    price_unit = fields.Float(related='product_id.lst_price')
    price_subtotal = fields.Monetary(compute='_compute_amount_t', string='Subtotal')
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('inprocess', 'Under Maintenance'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string="Status", default='draft', track_visibility='onchange')
    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account',
        readonly=False, copy=False, check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="The analytic account related to a sales order.")
#     states={'draft': [('readonly', False)], 'done': [('readonly', False)]},
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.company.currency_id.id)
#     price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    

   

    
    @api.depends('price_subtotal','price_unit')    
    def _compute_amount_t(self):
        for line in self:
#             line.price_subtotal = line.price_unit * line.demand_qty
#             t = line.price_unit
#             p = line.product_uom_qty
            line.update({
                'price_subtotal': line.price_unit * line.demand_qty
                
            })
    
#     @api.depends('product_qty', 'price_unit')
#     def _compute_amount(self):
#         for line in self:
#             vals = line._prepare_compute_all_values()
#             taxes = line.compute_all(
#                 vals['price_unit'],
#                 vals['currency_id'],
#                 vals['product_qty'],
#                 vals['product'],
#                 vals['partner'])
#             line.update({
#                 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
#                 'price_total': taxes['total_included'],
#                 'price_subtotal': taxes['total_excluded'],
#             })

#     def _prepare_compute_all_values(self):
#         # Hook method to returns the different argument values for the
#         # compute_all method, due to the fact that discounts mechanism
#         # is not implemented yet on the purchase orders.
#         # This method should disappear as soon as this feature is
#         # also introduced like in the sales module.
#         self.ensure_one()
#         return {
#             'price_unit': self.price_unit,
#             'currency_id': self.currency_id,
#             'product_qty': self.demand_qty,
#             'product': self.product_id,
#             'partner': self.order_id.partner_id,
#         }

   
    class MaintenanceOrder(models.Model):
        _inherit = 'maintenance.order'
        
        @api.model
        def _get_default_debit_account(self):
            return self.env['account.account'].search([
            ('name', '=', 'Accounts Receivable'),],
            limit=1).id
        
        @api.model
        def _get_default_credit_account(self):
            return self.env['account.account'].search([
            ('name', '=', 'Interest Receivable'),],
            limit=1).id
        
        @api.model
        def _get_default_journal(self):
            return self.env['account.journal'].search([
            ('name', '=', 'Miscellaneous Operations'),],
            limit=1).id
        

#         @api.depends('order_line.invoice_lines')
#         def _get_invoiced(self):
#         # The invoice_ids are obtained thanks to the invoice lines of the SO
#         # lines, and we also search for possible refunds created directly from
#         # existing invoices. This is necessary since such a refund is not
#         # directly linked to the SO.
#             for order in self:
#                 invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.type in ('out_invoice', 'out_refund'))
#                 order.invoice_ids = invoices
#                 order.invoice_count = len(invoices)
        
        def action_view_test(self):
            self.ensure_one()
            return {
            'type': 'ir.actions.act_window',
            'binding_type': 'object',
            'domain': [('name', '=', self.name)],   
            'multi': False,
            'name': 'Tasks',
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
        
#         @api.model
#         def _get_default_journal_entry(self):
#             test = self.env['account.move'].search([('name', 'in', self.name)],
#             limit=1).id
#             self.move_id = test
#             return test
        
        def get_bill_count(self):
            count = self.env['account.move'].search_count([('name', '=', self.name)])
            self.bill_count = count
        
        bill_count = fields.Integer(string='Sub Task', compute='get_bill_count')
        debit_account_id = fields.Many2one('account.account', related='maintenance_lines.account_id' )
        account_id = fields.Many2one('account.account', string='Credit Account')
        credit_account_id = fields.Many2one('account.account', string='Credit Account', default = _get_default_credit_account)
        journal_id = fields.Many2one('account.journal', string='Journal', default = _get_default_journal)
        amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',           tracking=True)
        amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
        amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
        currency_id = fields.Many2one('res.currency', 'Currency', required=True,
        default=lambda self: self.env.company.currency_id.id)
        move_id = fields.Many2one('account.move',string='Journal Entry',  domain="['|', ('company_id', '=', False), ('name', '=', name)]")

        
        

        @api.depends('maintenance_lines.price_subtotal')
        def _amount_all(self):
            for order in self:
                amount_untaxed = amount_tax = 0.0
                for line in order.maintenance_lines:
                    amount_untaxed += line.price_subtotal
#                     amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
#                 'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed 
            })
            
        
        def action_record_expense(self):
            debit_vals = {
                  'name': self.name,
                  'debit': abs(self.amount_total),
                  'credit': 0.0,
                  'account_id': self.maintenance_lines.account_id.id,
# #                   'tax_line_id': adjustment_type == 'debit' and self.tax_id.id or False,
                     }
            credit_vals = {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.amount_total),
                  'account_id': self.credit_account_id.id,
#                   'tax_line_id': adjustment_type == 'credit' and self.tax_id.id or False,
                  }
            vals = {
                  'name': self.name, 
                  'journal_id': self.journal_id.id,
                  'date': self.date_order,
                  'state': 'draft',
                  'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
                   }
            move = self.env['account.move'].create(vals)
            for line in self.maintenance_lines:
                for analytic_acc in line.analytic_account_id:
                    if  analytic_acc != '':
#                         num = 0
#                         for t in line.price_subtotal:
#                             num = num + t
                        analytic_vals = {
                          'name': self.name,
                          'amount': abs(line.price_subtotal),
                          'date': self.date_order,
                          'account_id': analytic_acc.id,
                          }
                        analytic = self.env['account.analytic.line'].create(analytic_vals)
                    else:
                        pass
#                 for analaytic_tags in line.analytic_tag_ids:
#                     if analaytic_tags.name != '':
#                         for i in analytic_tag_ids.analytic_distribution_ids:

                
                                    

        
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
