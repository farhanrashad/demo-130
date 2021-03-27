from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class EmployeeBadgePrint(models.Model):
    _inherit = 'hr.employee'

    # table 1 left side
#     gtn_number = fields.Char(string="GTN Number")
#     Project_name = fields.Char(string='Project Name')
#     mrf_ref_no = fields.Char(string='Mrf Ref No')
#     tower_type = fields.Char(string='Tower Type')
#     site_address = fields.Char(string=' Site Address')
#     contractor_name = fields.Char(string='Contractor Name')

  