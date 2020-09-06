# -*- coding: utf-8 -*-

from odoo import models, fields, api

class KraGroup(models.Model):
    _name = 'hr.kra.group'
    _description = 'KRA Group'
    
    name = fields.Char(required=True,string="Item")
    weightage = fields.Float(string="Weightage",required=True,)
    

class Kra(models.Model):
    _name = 'hr.kra'
    _description = 'Employee Key Results Areas'

    name = fields.Char(required=True,)
    kra_group_id = fields.Many2one('hr.kra.group', string='Group', required=True, ondelete='cascade', index=True, copy=False)
    kra_line = fields.One2many('hr.kra.line', 'kra_id', string='Kra Lines', )
    is_task = fields.Boolean(string="Is Task KRA",default=False)

    
class KraLine(models.Model):
    _name = 'hr.kra.line'
    _description = 'Employee KRA Line'
    
    kra_id = fields.Many2one('hr.kra', string='KRA Reference', required=True, ondelete='cascade', index=True, copy=False)
    name = fields.Char(required=True,string="Item")
    score = fields.Float(string="Score",required=True,)
    
    

