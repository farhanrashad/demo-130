# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PartnerModification(models.Model):
    _inherit = 'res.partner'
    
   
    

    @api.model
    def create(self,vals):
        vals['active'] = False
        res = super(PartnerModification,self).create(vals)
        return res
    
    
    def _calculate(self, qualify):
        if self.stage_id.is_quality == True:
           qualify = True                 
        return qualify
    
#      @api.model
    def write(self,vals):
        if self.stage_id.is_quality == True:
            vals['active'] = True    
        res = super(PartnerModification,self).write(vals)
        return res

    @api.onchange('stage_id')
    def _onchange_stage(self):
        if self.stage_id.is_quality == True:
	        self.active = True
       	
       	
    
    def _get_default_stage_id(self):
        stage = self.env['partner.stages'].search([], limit=1).id
        if stage:
            return stage
        else:
            return False
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['partner.stages'].search([])
        return stage_ids

    stage_id = fields.Many2one('partner.stages', string='Stage', ondelete='restrict', tracking=True, index=True, 
        group_expand='_read_group_stage_ids',
        default= _get_default_stage_id,                       
         copy=False) 
    


class PartnerStages(models.Model):
    _name = 'partner.stages'
    _description = 'Partner Stage'
    
    

    

    name = fields.Char(string='Stage Name', required=True, translate=True)
    user_id = fields.Many2one('res.users',string='User', store=True)
    is_quality = fields.Boolean(string='Quality')
    
