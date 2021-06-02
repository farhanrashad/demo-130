# -*- coding: utf-8 -*-
#################################################################################
# Author      : Dynexcel (<https://dynexcel.com/>)
# Copyright(c): 2015-Present dynexcel.com
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
from odoo.exceptions import Warning
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    
    def action_view_invoice(self):
        '''
        This function returns an action that display existing vendor bills of given purchase order ids.
        When only one found, show the vendor bill immediately.
        '''
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            'default_type': 'in_invoice',
            'default_company_id': self.company_id.id,
            'default_purchase_id': self.id,
        }
        # choose the view_mode accordingly
        if len(self.invoice_ids) > 1 and not create_bill:
            result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
        else:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                result['views'] = form_view
            # Do not set an invoice_id if we want to create a new bill.
            if not create_bill:
                result['res_id'] = self.invoice_ids.id or False
        result['context']['default_invoice_origin'] = self.name
        result['context']['default_ref'] = self.partner_ref
        result['context']['default_is_hide'] = True
        return result
    
    
    
    def send_approval_button(self):
        self.write({
            'state':'to approve'
        })
        
    def send_for_first_approval_button(self):
        self.write({
            'state':'waiting approval'
        })
    
    def first_approved_button(self):
        self.write({
            'state':'first approved'
        })
        self.send_approval_button()
    
    
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('waiting approval', 'Waiting First Approval'),
        ('first approved', 'First Approved'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    

class PaymentState(models.Model):
    _name = 'account.vendor_bill_state'
    _description = 'Vendor Bill State'

    name = fields.Char(string='Bill Status',help='maintain the states of the payment document')
    authority = fields.Many2one('res.groups')


class account_payment(models.Model):
    _inherit = 'account.move'
    
    state = fields.Selection([('draft', 'Draft'),
                              ('waiting', 'Waiting First Approval'),
                              ('waiting second approval', 'Waiting Second Approval'),
                              ('approved', 'Approved'),
                              ('posted', 'Posted'),
                              ('cancel','Cancelled') ],
                             readonly=True, default='draft', copy=False, string="Status", track_visibility='onchange')
    is_hide = fields.Boolean(default=False)
    
    
    def send_first_approval(self):
        self.write({'state': 'waiting'})
        self.message_post(body=_('Dear %s, bill is sent for approval.') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])
        
    def action_reset_draft(self):
        self.write({'state': 'draft'})
        self.message_post(body=_('Dear %s, bill is Rejected from Approval.') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])

    def first_approve_bill(self):
        self.write({'state': 'waiting second approval'})
        self.message_post(body=_('Dear %s, bill has approved.') % (self.env.user.name,),
                          partner_ids=[self.env.user.partner_id.id])


    def second_approve_bill(self):
        self.action_post()
        
        
    def action_post(self):
        self.message_post(body=_('Dear %s, bill has posted') % (self.env.user.name,),
                              partner_ids=[self.env.user.partner_id.id])
        res = super(account_payment, self).action_post()
      
        return res