# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MaintenanceOrder(models.Model):
    _inherit = 'maintenance.order.line'
    
    @api.model
    def _get_default_account(self):
        return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
    
    account_id = fields.Many2one('account.account', string='Account',
        index=True, ondelete="restrict", check_company=True,
        domain=[('deprecated', '=', False)],  default = _get_default_account )
    price_unit = fields.Float(related='product_id.standard_price')
    price_subtotal = fields.Monetary(compute='_compute_amount_t', string='Subtotal')
    company_id = fields.Many2one('res.company', string='Company')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('inprocess', 'Under Maintenance'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string="Status", default='draft', track_visibility='onchange')
    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account',
        readonly=False, copy=False, check_company=True, 
        help="The analytic account related to a sales order.")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    currency_id = fields.Many2one('res.currency', 'Currency')

    

   

    
    @api.depends('price_subtotal','price_unit', 'demand_qty')    
    def _compute_amount_t(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.demand_qty

    
                

    

   
    class MaintenanceOrder(models.Model):
        _inherit = 'maintenance.order'
        
        @api.model
        def _get_default_debit_account(self):
            return self.env['account.account'].search([
            ('name', '=', 'Cost of Goods Sold'),],
            limit=1).id
        
        @api.model
        def _get_default_credit_account(self):
            return self.env['account.account'].search([
            ('name', '=', 'Stock Valuation Account'),],
            limit=1).id
        
        @api.model
        def _get_default_journal(self):
            return self.env['account.journal'].search([
            ('name', '=', 'Miscellaneous Operations'),],
            limit=1).id
        

        
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
        currency_id = fields.Many2one('res.currency', 'Currency')
        move_id = fields.Many2one('account.move',string='Journal Entry',  domain="['|', ('company_id', '=', False), ('name', '=', name)]")

        
        

        @api.depends('maintenance_lines.price_subtotal')
        def _amount_all(self):
            for order in self:
                amount_untaxed = amount_tax = 0.0
                for line in order.maintenance_lines:
                    amount_untaxed += line.price_subtotal
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_total': amount_untaxed 
            })
            
        
        def action_record_expense(self):
            for oline in self.maintenance_lines:                
            	debit_vals = {
                  	'name': self.name,
                  	'debit': abs(self.amount_total),
                  	'credit': 0.0,
                  	'analytic_account_id': oline.analytic_account_id.id,   
                  	'account_id': self.debit_account_id.id,
                     }
            credit_vals = {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.amount_total),
                  'account_id': self.credit_account_id.id,
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
                        analytic_vals = {
                          'name': self.name,
                          'amount': abs(line.price_subtotal),
                          'unit_amount': line.demand_qty,
                          'product_id': line.product_id.id,
                          'general_account_id': line.account_id.id,
                          'date': self.date_order,
                          'account_id': analytic_acc.id,
                          }
                        analytic = self.env['account.analytic.line'].create(analytic_vals)
                    else:
                        pass
                for analaytic_tags in line.analytic_tag_ids:
                    if analaytic_tags.name != '':
                        for i in analaytic_tags.analytic_distribution_ids:
                            for n in i.account_id:
                                if n !='':
                                    analytic_tags = {
                                      'name': self.name,
                                      'amount': abs((line.price_subtotal) * (i.percentage/100)),
                                      'unit_amount': line.demand_qty,
                                      'product_id': line.product_id.id,
                                      'general_account_id': line.account_id.id,
                                      'date': self.date_order,
                                      'account_id': n.id,
                                          }
                                    analytic = self.env['account.analytic.line'].create(analytic_tags)
                                else:
                                    pass
                    else:
                        pass

                
                                    

        

