from datetime import datetime
from odoo import api, fields, models, _


class  HrApplicant(models.Model):
    _inherit='hr.applicant'

    applicant_city = fields.Char(string='City')