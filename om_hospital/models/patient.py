# -*- coding: utf-8 -*-
from odoo import models, fields, _
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class HospitalPatient(models.Model):
    _inherit = "sale.order"
    
    Patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread.cc','mail.activity.mixin']
    _description = "Hospital Patient"
    
    
    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age < 5:
                raise UserError('Age must be greater then 5')
    
#     @api.depends('age_group')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'
   
    
    
    name = fields.Char(string='Name', required=True , track_visibility="always")
    patient_age = fields.Integer(string='Age', track_visibility="always")
    gender = fields.Selection([
         ('male', 'Male'),
         ('female', 'Female'),
         ('other', 'other'),
     ], required=True, default='male')
    age_group = fields.Selection([
         ('major', 'Major'),
         ('minor', 'Minor'),
    ], string="Age Group", compute='set_age_group')
    test = fields.Char(string='Test')
    note = fields.Text(string='Registration Note')
    image = fields.Binary(string="Upload Image")
    
#   only name_seq field for page sequence on form
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
    
    
#   compute method for set age minor or major on the base of condition
   

