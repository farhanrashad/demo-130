# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerModification(models.Model):
    _inherit = 'res.partner'
    
    def _get_default_stage_id(self):
        return self.env['partner.stages'].search([], limit=1).id
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['partner.stages'].search([])
        return stage_ids

    stage_id = fields.Many2one('partner.stages', string='Stage', ondelete='restrict', tracking=True, index=True, copy=False) 
        # group_expand='_read_group_stage_ids',
        # default=_get_default_stage_id,
         
    
    
class PartnerStages(models.Model):
    _name = 'partner.stages'
    _description = 'Partner Stage'
    
    

    def _get_default_project_ids(self):
        default_project_id = self.env.context.get('default_project_id')
        return [default_project_id] if default_project_id else None

    name = fields.Char(string='Stage Name', required=True, translate=True)
    user_id = fields.Many2one('res.users',string='User', store=True)
    is_quality = fields.Boolean(string='Quality')
    
