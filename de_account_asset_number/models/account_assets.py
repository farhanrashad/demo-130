# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    @api.model
    def _get_sequence_prefix(self, code, refund=False):
        prefix = code.upper()
        if refund:
            prefix = 'R' + prefix
        return prefix + '/%(range_year)s/'
    
    
    @api.model
    def _create_sequence(self, vals, refund=False):
        """ Create new no_gap entry sequence for every new Asset"""
        prefix = self._get_sequence_prefix(vals['code'], refund)
        seq_name = vals['code']
        seq = {
            'name': _('%s Sequence') % seq_name,
            'implementation': 'no_gap',
            'prefix': prefix,
            'padding': 4,
            'number_increment': 1,
            'use_date_range': True,
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        seq = self.env['ir.sequence'].create(seq)
        seq_date_range = seq._get_current_sequence()
        seq_date_range.number_next = vals.get('sequence_number_next', 1)
        return seq

    
    @api.model
    def create(self,vals):
        if vals.get('code',_('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('account.asset') or _('New')
        if not vals.get('sequence_id'):
            vals.update({'sequence_id': self.sudo()._create_sequence(vals).id})    
            
        res = super(AccountAsset,self).create(vals)
        return res
    
    
    
    
    

    code = fields.Char(string='Number', required=True, readonly="1", copy=False, default='1')
    sequence_number_next = fields.Integer(string='Next Number',
        help='The next sequence number will be used for the next invoice.',
        compute='_compute_seq_number_next',
        inverse='_inverse_seq_number_next')
    sequence_id = fields.Many2one('ir.sequence', string='Entry Sequence',
        help="This field contains the information related to the numbering of the journal entries of this Asset.",  copy=False)
    
    
    @api.depends('sequence_id.use_date_range', 'sequence_id.number_next_actual')
    def _compute_seq_number_next(self):
        '''Compute 'sequence_number_next' according to the current sequence in use,
        an ir.sequence or an ir.sequence.date_range.
        '''
        for asset in self:
            if asset.sequence_id:
                sequence = asset.sequence_id._get_current_sequence()
                asset.sequence_number_next = sequence.number_next_actual
            else:
                asset.sequence_number_next = 1

    def _inverse_seq_number_next(self):
        '''Inverse 'sequence_number_next' to edit the current sequence next number.
        '''
        for asset in self:
            if asset.sequence_id and asset.sequence_number_next:
                sequence = asset.sequence_id._get_current_sequence()
                sequence.sudo().number_next = asset.sequence_number_next

    
    
  