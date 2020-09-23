# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    @api.model
    def create(self,vals):
        if vals.get('code',_('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('account.asset') or _('New')    
        res = super(AccountAsset,self).create(vals)
        return res
    
    

    code = fields.Char(string='Number', required=True, readonly=True, copy=False, default='/')
    sequence_number_next = fields.Integer(string="Next Number")
    sequence_id = fields.Many2one('ir.sequence',string="Sequence")

    