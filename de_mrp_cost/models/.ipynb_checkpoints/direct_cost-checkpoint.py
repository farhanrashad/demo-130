# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_charge = fields.Boolean(string='Is Charge', store=True)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    def button_generate_bill(self):
        vendor_list = []
        for line in self.cost_lines:
            if line.partner_id and line.is_billed == False:
                vendor_list.append(line.partner_id)
            else:
                pass
        list = set(vendor_list)
        for partner in list:
            product_list = []
            for line in self.cost_lines:
                if partner == line.partner_id:
                    if line.is_billed == False:
                        valss = {
                            'product_id': line.product_id.id,
                            'name': line.product_id.name,
                            'account_id': line.account_id.id,
                            'price_unit': line.product_id.standard_price,
                            'partner_id': line.partner_id.id,
                            'product_uom_id': line.product_id.uom_po_id.id,
                        }
                        product_list.append(valss)
#             vals = {
#                   'partner_id': partner.id,
#                   'journal_id': self.journal_id.id,
#                   'invoice_date': fields.Date.today(),
#                   'type': 'out_invoice',
#                   'invoice_origin': self.id,
#                     }
#             move = self.env['account.move'].create(vals)
            move_dict = {
                  'partner_id': partner.id,
                  'journal_id': self.journal_id.id,
                  'invoice_date': fields.Date.today(),
                  'type': 'in_invoice',
                  'invoice_origin': self.name,
                   }
               
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            sum_tot_amount = 0.0
            
                        #step2:debit side entry
            for oline in self.cost_lines:
                sum_tot_amount = sum_tot_amount + oline.standard_price 
                debit_line = (0, 0, {
    #                  	'move_id': move.id,
                    'name': oline.product_id.name,
                    'debit': abs(oline.standard_price),
                    'credit': 0.0,
                    'account_id': oline.account_id.id,
                         })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                #step3:credit side entry
            credit_line = (0, 0, {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(sum_tot_amount),
                  'account_id': self.credit_account_id.id,
                          })
            line_ids.append(credit_line)
            credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            
            move_dict['invoice_line_ids'] = product_list
#             move_dict['line_ids'] = line_ids

            move = self.env['account.move'].create(move_dict)

        
#             for product in product_list:
#                 move_line = {
#                        'move_id': move.id,
#                        'product_id': product['product_id'],
#                        'name': product['name'],
#                        'account_id': product['account_id'],
#                        'price_unit': product['price_unit'],
#                        'partner_id': product['partner_id'],
                        
#                        'product_uom_id': product['product_uom_id'],
#                         }
#                 orders_lines = self.env['account.move.line'].create(move_line)
#         self.partner_id= False

        for line in self.cost_lines:
            if line.is_billed == False and line.partner_id:
                line.update ({
#                    'po_process': False,
                    'is_billed': True,
                  	})    
    
    credit_account_id = fields.Many2one('account.account', string='Credit Account', required=True)    
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    cost_lines = fields.One2many('mrp.production.direct.cost', 'production_id' ,string='Direct Cost Lines')    
    
    
class MrpCost(models.Model):
    _name = 'mrp.production.direct.cost'
    _description = 'This Production Order Cost'

    product_id = fields.Many2one('product.product',string='Product', domain="[('type', '=', 'service')]")
    account_id = fields.Many2one('account.account', string='Account', required=True)
    production_id = fields.Many2one('mrp.production', string="Manufacturing Order")
    is_charge = fields.Boolean(related='product_id.is_charge')
    standard_price = fields.Float(related='product_id.standard_price', readonly=False)
    is_billed = fields.Boolean(string='Billed', readonly=True)
    partner_id = fields.Many2one('res.partner', related='product_id.seller_ids.name',readonly=False)
    

