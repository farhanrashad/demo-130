# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrTrainingCoordinator(models.Model):
    _name = 'hr.training.coordinator'
    _description = 'This is a model for Coordinator in HR Training Module'
    _rec_name = 'name'

    @api.model
    def create(self, vals):
        if vals.get('coordinator_seq', _('No ID')) == _('No ID'):
            vals['coordinator_seq'] = self.env['ir.sequence'].next_by_code('hr.training.coordinator') or _(
                'No ID')
            result = super(HrTrainingCoordinator, self).create(vals)
            return result

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    description = fields.Text(string='Description')
    coordinator_seq = fields.Char(string='Coordinator ID', required=True, Readonly=True, copy=False, index=True,
                                  default=lambda self: _('No ID'))
