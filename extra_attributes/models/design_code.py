# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies

from odoo import models,fields,api,_

class DesignCode(models.Model):
    _name='design.code'
    _description='Design Code'
    _rec_name ='name'
    
    name=fields.Char("Design Code",required=True)