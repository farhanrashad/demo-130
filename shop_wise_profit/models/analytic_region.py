# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class AnalyticRegion(models.Model):
    _name = 'analytic.region'

    name = fields.Char()

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    region_id = fields.Many2one('analytic.region', 'Region')
