# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    visa_lines = fields.One2many('visa.card.details', 'visa_id')

    passport_number = fields.Char(String="Passport Number")
    passport_issue_date = fields.Date(String="Passport Issue Date")
    passport_expiry_date = fields.Date(String="Passport Expiry Date")
    passport_country = fields.Many2one('res.country',String="Passport Expiry Date")
    other_nationality = fields.Many2many('res.country',string="Other Nationality")
    # visa fields record


class VisaCardDetails(models.Model):
    _name = 'visa.card.details'
    _description = 'Visa Card Details'

    stats = fields.Selection([('to_request', 'To Request'), ('in_process', 'In Process'), ('approve', 'Approve'), ('reject', 'Reject'), ('expired', 'Expired')], string='state', default='to_request')
    visa_id = fields.Many2one('hr.employee',String="Visa Id")
    description = fields.Char(string="Description")
    visa_Type = fields.Char(string="Visa Type")
    Visa_issuance_Date = fields.Date(string="Issuance Date")
    Visa_Expiration_Date = fields.Date(string="Expiration Date")
    Visa_country = fields.Many2one('res.country',string="Country")
    no_of_entries = fields.Char(string="No. Of Entries")
    status = fields.Char(string="Status")