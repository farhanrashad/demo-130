#-*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskSite(models.Model):
    _inherit = "helpdesk.ticket"

    distributor = fields.Char('Distributor', index=True)
    site_name = fields.Char('Site Name', index=True)
    contact_name = fields.Char('Contact Name')
    contact_no = fields.Char('Contact no')
    site_address = fields.Char('Site Address')
    
    city = fields.Char('City')
    
    reference = fields.Char('Reference')
    
    material = fields.Char('Material To Equipment')
    barcode = fields.Char('Barcode/Serial')
    model = fields.Char('Model')
    
    customer_model_desc = fields.Char('Customer Model Desc')
    reason = fields.Text('Reason')
    crmid = fields.Char('CRM ID')
    serial = fields.Char('Barcode/Serial')  
    
    @api.depends('serial')
    @api.onchange('serial')
    def _compute_field(self):
        for sd in self:
            jj=self.env['stock.production.lot'].search([('name','=',sd.serial)])
            if sd.serial:
                m=jj.product_id.id
                sd.product_id=m
            else:
                sd.product_id=''
    
    
    @api.constrains('name', 'stage_id')
    def _check_unique_sequence_number(self):
        moves = self.filtered(lambda move: move.stage_id.name == 'posted')
        if not moves:
            return
        self.flush()