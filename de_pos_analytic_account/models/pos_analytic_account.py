from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class PosConfigInherit(models.Model):
    _inherit = 'pos.config'

    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account")

