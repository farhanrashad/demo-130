# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class DxlReportState(models.Model):
    _name = 'dxl.report.state'

    name = fields.Char()
    code = fields.Char()
