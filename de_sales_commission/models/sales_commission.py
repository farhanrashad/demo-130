# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import chain

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.misc import get_lang

from odoo.addons import decimal_precision as dp

class SalesCommission(models.Model):
    _name = 'sale.commission'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Sale Commission"
    _order = 'doc_date desc, id desc'

    def action_created_invoice_commission(self):
        self.ensure_one()
        return {
            'name': _('Invoice created'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.move',
            'view_id': self.env.ref('account.view_move_form').id,
            'target': 'current',
            'res_id': self.invoice_id.id,
              }
    
    @api.model
    def _default_product_id(self):
        product_id = self.env['ir.config_parameter'].sudo().get_param('sale.default_commission_product_id')
        return self.env['product.product'].browse(int(product_id)).exists()
    

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, state={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    currency_id = fields.Many2one("res.currency", string="Currency", required=True, readonly=True, states={'draft': [('readonly', False)]}, )
    # partner_invoice_id = fields.Many2one('res.partner', 'Invoicing Address')

    invoice_id = fields.Many2one(
        'account.move', 'Invoice',
        copy=False, readonly=True, tracking=True,
        domain=[('type', '=', 'out_invoice')])
    agent_id = fields.Many2one('res.partner', string='Agent', required=True, help="Commission Agent", readonly=True, states={'draft': [('readonly', False)]}, )
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange', track_sequence=2, default=lambda self: self.env.user)
    
    doc_date = fields.Datetime(string='Date', required=True, index=True, copy=False, default=fields.Datetime.now, readonly=True, states={'draft': [('readonly', False)]}, )
    product_id = fields.Many2one('product.product', string='Product', domain=[('type', '=', 'service')],
                                 readonly=True, states={'draft': [('readonly', False)]}, default=_default_product_id)
    # required = True,
    commission_amount = fields.Float(string='Comm. Amount',required=True, readonly=True, states={'draft': [('readonly', False)]}, )
    sale_id = fields.Many2one('sale.order', 'Sale Order',required=False, domain="[('state', 'in', ['sale','done'])]", readonly=True, states={'draft': [('readonly', False)]}, )
    sale_amount = fields.Monetary(string='Total Sale', related='sale_id.amount_total', store=True, readonly=True, )
    # invoiced = fields.Boolean('Invoiced', copy=False, readonly=True)

    is_invoiced = fields.Boolean('Is Invoiced', default=False, readonly=True)
    invoice_id = fields.Many2one('account.move', 'Invoice',required=False,  readonly=True, )
    date_invoiced = fields.Datetime(string='Date Invoiced', required=False, readonly=True)
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('sale.commission') 
        values['name'] = seq
        res = super(SalesCommission,self).create(values)
        return res
    
    def action_confirm(self):
        self.state = 'posted'

    def action_commission_invoice_create(self):
        for repair in self:
            repair._create_invoices_commission()
            # if repair.state == 'paid':
                # repair.action_repair_ready()
            if repair.state == 'cancel':
                repair.write({'state': 'cancel'})
        return True

    def _create_invoices_commission(self, group=False):

        grouped_invoices_vals = {}
        repairs = self.filtered(lambda repair: repair.state not in ('draft', 'cancel')
                                               # below i will comment invoice_id which will prevent to create second invoice
                                               # ===========================================================================
                                               # and not repair.invoice_id
                                               # and repair.state != 'cancel'
                                )
        for repair in repairs:
            partner_invoice = repair.agent_id
            if not partner_invoice:
                raise UserError(_('You have to select an invoice address in the repair form.'))

            currency = repair.currency_id
            # Fallback on the user company as the 'company_id' is not required.
            company = repair.company_id or self.env.user.company_id

            journal = self.env['account.move'].with_context(force_company=company.id,
                                                            type='out_invoice')._get_default_journal()
            if not journal:
                raise UserError(_('Please define an accounting sales journal for the company %s (%s).') % (
                    self.company_id.name, self.company_id.id))

            if (partner_invoice.id, currency.id) not in grouped_invoices_vals:
                grouped_invoices_vals[(partner_invoice.id, currency.id)] = []
            current_invoices_list = grouped_invoices_vals[(partner_invoice.id, currency.id)]

            if not group or len(current_invoices_list) == 0:
                fp_id = repair.agent_id.property_account_position_id.id or self.env[
                    'account.fiscal.position'].get_fiscal_position(repair.agent_id.id,
                                                                   delivery_id=repair.agent_id.id)
                invoice_vals = {
                    'type': 'out_invoice',
                    'partner_id': partner_invoice.id,
                    'currency_id': currency.id,
                    # 'narration': narration,
                    'line_ids': [],
                    'invoice_origin': repair.name,
                    # 'repair_ids': [(4, repair.id)],
                    'invoice_line_ids': [],
                    'fiscal_position_id': fp_id
                }
                current_invoices_list.append(invoice_vals)
            else:
                # if group == True: concatenate invoices by partner and currency
                invoice_vals = current_invoices_list[0]
                invoice_vals['invoice_origin'] += ', ' + repair.name
                # invoice_vals['repair_ids'].append((4, repair.id))
                # if not invoice_vals['narration']:
                #     invoice_vals['narration'] = narration
                # else:
                #     invoice_vals['narration'] += '\n' + narration

            # Create invoice lines from operations.
            # for operation in repair.operations.filtered(lambda op: op.type == 'add'):
            #     if group:
            #         name = repair.name + '-' + operation.name
            #     else:
            #         name = operation.name
            #
            #     account = operation.product_id.product_tmpl_id._get_product_accounts()['income']
            #     if not account:
            #         raise UserError(_('No account defined for product "%s".') % operation.product_id.name)

                invoice_line_vals = {
                    # 'name': name,
                    # 'account_id': account.id,
                    # 'quantity': operation.product_uom_qty,
                    # 'tax_ids': [(6, 0, operation.tax_id.ids)],
                    # 'product_uom_id': operation.product_uom.id,
                    # 'price_unit': operation.price_unit,
                    # 'product_id': operation.product_id.id,
                    # 'repair_line_ids': [(4, operation.id)],
                }

                if currency == company.currency_id:
                    # balance = -(operation.product_uom_qty * operation.price_unit)
                    invoice_line_vals.update({
                        # 'debit': balance > 0.0 and balance or 0.0,
                        # 'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    # amount_currency = -(operation.product_uom_qty * operation.price_unit)
                    balance = currency._convert(self.company_id.currency_id, self.company_id,
                                                fields.Date.today())
                    invoice_line_vals.update({
                        # 'amount_currency': amount_currency,
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                        'currency_id': currency.id,
                    })
                invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

            # Create invoice lines from fees.

        # Create invoices.
        invoices_vals_list = []
        for invoices in grouped_invoices_vals.values():
            for invoice in invoices:
                invoices_vals_list.append(invoice)
        self.env['account.move'].with_context(default_type='out_invoice').create(invoices_vals_list)

        repairs.write({'is_invoiced': True})  #
        # repairs.mapped('operations').filtered(lambda op: op.type == 'add').write({'invoiced': True})  #
        # repairs.mapped('fees_lines').write({'invoiced': True})
        return dict((repair.id, repair.invoice_id.id) for repair in repairs)

        # this below method call in above operation page function
        # ===========================================================================


    def action_commission_invoice_create(self):
        self.state = 'paid'
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def unlink(self):
        for rs in self:
            if rs.state not in ('draft'):
                raise UserError(_('You can not delete a posted document.'))
        return super(SalesCommission, self).unlink()
    