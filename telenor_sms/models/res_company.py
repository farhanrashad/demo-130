# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    msisdn = fields.Char('MSISDN')
    password = fields.Char('Password')
    mask = fields.Char('Mask')
