from datetime import datetime
from odoo import api, fields, models, _


class  HrApplicant(models.Model):
    _inherit='hr.applicant'

    applicant_city = fields.Char(string='City')
    applicant_education = fields.Char(string='Education')
    applicant_position = fields.Char(string='Current/Last Position')