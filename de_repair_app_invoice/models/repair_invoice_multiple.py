from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare
from itertools import groupby

class RepairInvoice(models.Model):
    _inherit = 'repair.order'

    def get_invoice_count(self):
        count = self.env['account.move'].search_count([('invoice_origin', '=', self.name)])
        self.invoice_count = count

    invoice_count = fields.Integer(compute="get_invoice_count")
    # , copy = False, default = 0, store = True



 #=======================================================
    #this is invoice view code for multiple invoices
#========================================================
    def action_created_invoice(self):
        self.ensure_one()
        return {
            'name': _('Invoice created'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            # 'view_id': self.env.ref('account.view_move_form').id,
            # 'target': 'current',
            'domain': [('invoice_origin', '=', self.name)],
            'res_id': self.invoice_id.id,
            'context': dict(self._context, create=False, default_company_id=self.company_id.id,)

        }


    # ==========================================================================
    def action_repair_part_invoice_create(self):
        for repair in self:
            repair._create_invoices_part()
            if repair.invoice_method == 'b4repair':
                repair.action_repair_ready()
            elif repair.invoice_method == 'after_repair':
                repair.write({'state': 'done'})
        return True



    # operation invoice function
    # =======================================================================

    def action_repair_operations_invoice_create(self):
        for repair in self:
            repair._create_invoices_operation()
            if repair.invoice_method == 'b4repair':
                repair.action_repair_ready()
            elif repair.invoice_method == 'after_repair':
                repair.write({'state': 'done'})
        return True

    #  this method call in above part function
    # ==========================================================================
    def _create_invoices_part(self, group=False):

        grouped_invoices_vals = {}
        repairs = self.filtered(lambda repair: repair.state not in ('draft', 'cancel')
         # below i will comment invoice_id which will prevent to create second invoice
           # ===========================================================================
                                               # and not repair.invoice_id
                                               and repair.invoice_method != 'none')
        for repair in repairs:
            partner_invoice = repair.partner_invoice_id or repair.partner_id
            if not partner_invoice:
                raise UserError(_('You have to select an invoice address in the repair form.'))

            narration = repair.quotation_notes
            currency = repair.pricelist_id.currency_id
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
                fp_id = repair.partner_id.property_account_position_id.id or self.env[
                    'account.fiscal.position'].get_fiscal_position(repair.partner_id.id,
                                                                   delivery_id=repair.address_id.id)
                invoice_vals = {
                    'type': 'out_invoice',
                    'partner_id': partner_invoice.id,
                    'currency_id': currency.id,
                    'narration': narration,
                    'line_ids': [],
                    'invoice_origin': repair.name,
                    'repair_ids': [(4, repair.id)],
                    'invoice_line_ids': [],
                    'fiscal_position_id': fp_id
                }
                current_invoices_list.append(invoice_vals)
            else:
                # if group == True: concatenate invoices by partner and currency
                invoice_vals = current_invoices_list[0]
                invoice_vals['invoice_origin'] += ', ' + repair.name
                invoice_vals['repair_ids'].append((4, repair.id))
                if not invoice_vals['narration']:
                    invoice_vals['narration'] = narration
                else:
                    invoice_vals['narration'] += '\n' + narration

            # Create invoice lines from operations.
            for operation in repair.operations.filtered(lambda op: op.type == 'add'):
                if group:
                    name = repair.name + '-' + operation.name
                else:
                    name = operation.name

                account = operation.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".') % operation.product_id.name)

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': operation.product_uom_qty,
                    'tax_ids': [(6, 0, operation.tax_id.ids)],
                    'product_uom_id': operation.product_uom.id,
                    'price_unit': operation.price_unit,
                    'product_id': operation.product_id.id,
                    'repair_line_ids': [(4, operation.id)],
                }

                if currency == company.currency_id:
                    balance = -(operation.product_uom_qty * operation.price_unit)
                    invoice_line_vals.update({
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    amount_currency = -(operation.product_uom_qty * operation.price_unit)
                    balance = currency._convert(amount_currency, self.company_id.currency_id, self.company_id,
                                                fields.Date.today())
                    invoice_line_vals.update({
                        'amount_currency': amount_currency,
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

        repairs.write({'invoiced': True}) #
        repairs.mapped('operations').filtered(lambda op: op.type == 'add').write({'invoiced': True}) #
        # repairs.mapped('fees_lines').write({'invoiced': True})
        return dict((repair.id, repair.invoice_id.id) for repair in repairs)

    # this below method call in above operation page function in fee_lines in repair order
    # ===========================================================================

    def _create_invoices_operation(self, group=False):

        grouped_invoices_vals = {}
        repairs = self.filtered(lambda repair: repair.state not in ('draft', 'cancel')
        # below i will comment invoice_id which will prevent to create second invoice
        #===========================================================================
                                               # and not repair.invoice_id
                                               and repair.invoice_method != 'none')
        for repair in repairs:
            partner_invoice = repair.partner_invoice_id or repair.partner_id
            if not partner_invoice:
                raise UserError(_('You have to select an invoice address in the repair form.'))

            narration = repair.quotation_notes
            currency = repair.pricelist_id.currency_id
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
                fp_id = repair.partner_id.property_account_position_id.id or self.env[
                    'account.fiscal.position'].get_fiscal_position(repair.partner_id.id,
                                                                   delivery_id=repair.address_id.id)
                invoice_vals = {
                    'type': 'out_invoice',
                    'partner_id': partner_invoice.id,
                    'currency_id': currency.id,
                    'narration': narration,
                    'line_ids': [],
                    'invoice_origin': repair.name,
                    'repair_ids': [(4, repair.id)],
                    'invoice_line_ids': [],
                    'fiscal_position_id': fp_id
                }
                current_invoices_list.append(invoice_vals)
            else:
                # if group == True: concatenate invoices by partner and currency
                invoice_vals = current_invoices_list[0]
                invoice_vals['invoice_origin'] += ', ' + repair.name
                invoice_vals['repair_ids'].append((4, repair.id))
                if not invoice_vals['narration']:
                    invoice_vals['narration'] = narration
                else:
                    invoice_vals['narration'] += '\n' + narration

            # Create invoice lines from fees.
            for fee in repair.fees_lines:
                if group:
                    name = repair.name + '-' + fee.name
                else:
                    name = fee.name

                if not fee.product_id:
                    raise UserError(_('No product defined on fees.'))

                account = fee.product_id.product_tmpl_id._get_product_accounts()['income']
                if not account:
                    raise UserError(_('No account defined for product "%s".') % fee.product_id.name)

                invoice_line_vals = {
                    'name': name,
                    'account_id': account.id,
                    'quantity': fee.product_uom_qty,
                    'tax_ids': [(6, 0, fee.tax_id.ids)],
                    'product_uom_id': fee.product_uom.id,
                    'price_unit': fee.price_unit,
                    'product_id': fee.product_id.id,
                    'repair_fee_ids': [(4, fee.id)],
                }

                if currency == company.currency_id:
                    balance = -(fee.product_uom_qty * fee.price_unit)
                    invoice_line_vals.update({
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                    })
                else:
                    amount_currency = -(fee.product_uom_qty * fee.price_unit)
                    balance = currency._convert(amount_currency, self.company_id.currency_id, self.company_id,
                                                fields.Date.today())
                    invoice_line_vals.update({
                        'amount_currency': amount_currency,
                        'debit': balance > 0.0 and balance or 0.0,
                        'credit': balance < 0.0 and -balance or 0.0,
                        'currency_id': currency.id,
                    })
                invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

        # Create invoices.
        invoices_vals_list = []
        for invoices in grouped_invoices_vals.values():
            for invoice in invoices:
                invoices_vals_list.append(invoice)
        self.env['account.move'].with_context(default_type='out_invoice').create(invoices_vals_list)

        repairs.write({'invoiced': True}) #
        # repairs.mapped('operations').filtered(lambda op: op.type == 'add').write({'invoiced': True})
        repairs.mapped('fees_lines').write({'invoiced': True}) #

        return dict((repair.id, repair.invoice_id.id) for repair in repairs)


