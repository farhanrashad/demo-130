from odoo import models, fields, api


class Requisitiesboq(models.Model):
    _name = 'boq.boq'
    _description = 'this is boq model'

    name = fields.Char(string='Name')


class Materials(models.Model):
    _name = 'materials.materials'
    _description = 'this is materials model'

    name = fields.Char(string='Name')
