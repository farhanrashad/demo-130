from odoo import models, fields, api

class Contractors(models.Model):
    _name = 'contractor.contractor'
    _description = 'this is contractor process model'

    name = fields.Char(string='Name')