# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo import exceptions 


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, values):
        t_uid = self.env.uid
        if t_uid == 25 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors')
        if t_uid == 12 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors')
        if t_uid == 14 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors')
        elif t_uid == 11 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors')
        elif t_uid == 19 : 
            raise exceptions.ValidationError('You are not allowed to create customers / vendors')    
        res = super(ResPartner, self).create(values)
        return res
    
    
    @api.multi
    def write(self, values):
        t_uid = self.env.uid
        if t_uid == 25 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors')
        if t_uid == 12 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors')
        if t_uid == 14 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors')
        elif t_uid == 11 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors') 
        elif t_uid == 19 : 
            raise exceptions.ValidationError('You are not allowed to update customers / vendors')    
        res = super(ResPartner, self).write(values)
        return res

