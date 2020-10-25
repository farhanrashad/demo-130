from odoo import models, fields, api

class Stagesconf(models.Model):
    _name = 'stages.stages'
    _description = 'this is staging process model'

    name = fields.Char(string='Name')
