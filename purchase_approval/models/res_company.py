# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    purchase_approval = fields.Boolean('Purchase Approval')
