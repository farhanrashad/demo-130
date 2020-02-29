# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrTrainingSubject(models.Model):
    _name = 'hr.training.subject'
    _description = 'This is a model for Subjects in HR Training Module'
    _rec_name = 'title'

    @api.model
    def create(self, vals):
        if vals.get('subject_seq', _('No ID')) == _('No ID'):
            vals['subject_seq'] = self.env['ir.sequence'].next_by_code('hr.training.subject') or _(
                'No ID')
            result = super(HrTrainingSubject, self).create(vals)
            return result

    title = fields.Char(string='Title', required=True)
    coordinator = fields.Many2one('hr.training.coordinator', string='Coordinator')
    description = fields.Text(string='Description')
    subject_seq = fields.Char(string='Session ID', required=True, Readonly=True, copy=False, index=True,
                              default=lambda self: _('No ID'))
