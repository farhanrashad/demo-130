#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSite(models.Model):
    _inherit = "helpdesk.ticket"

    site_name = fields.Char('Site Name', index=True)
    contact_name = fields.Char('Contact Name')
    site_address = fields.Char('Site Address')
    region = fields.Char('region')
    city = fields.Char('city')
    
    material = fields.Char('Material')
    barcode = fields.Char('Barcode/Serial')
    model = fields.Char('Model')