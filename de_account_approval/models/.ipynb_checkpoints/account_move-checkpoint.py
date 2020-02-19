# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting For Approval'), ('accountant_approved', 'Approved'), ('manager_approved', 'Approved'), ('rejected', 'Rejected'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    
    def action_submit(self):
        for move in self:
            if not move.line_ids.filtered(lambda line: not line.display_type):
                raise UserError(_('You need to add a line before posting.'))
        self.write({
            'state':'waiting_approval',
        })
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'move_id':self.id,
            'status':'Prepared By'
        })
        self.message_post(body=_('Document has submitted by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
        
    def action_approve_accountant(self):
        self.write({
            'state':'accountant_approved',
        })
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'move_id':self.id,
            'status':'Reviewed By'
        })
        self.message_post(body=_('Document has reviewed by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
    
    def action_approve_manager(self):
        self.write({
            'state':'manager_approved',
        })
        self.post()
        self.env['account.approval.log'].sudo().create({
            'user_id':self.env.user.id,
            'move_id':self.id,
            'status':'Approved By'
        })
        self.message_post(body=_('Document has approved and posted by %s,') % (self.env.user.name, ),
                  partner_ids=[self.env.user.partner_id.id])
        
    def action_reject(self):
        self.write({
            'state':'rejected',
            'approval_level':self.approval_level-1,
        })