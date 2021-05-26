# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import date, time, datetime

class AccountBankStatementCashbox(models.Model):
    _inherit = 'account.bank.statement.cashbox'

    is_pos_manager = fields.Boolean()

    @api.model
    def default_get(self, fields):
        session_id = self.env.context.get('pos_session_id')
        vals = super(AccountBankStatementCashbox, self).default_get(fields)
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if session_id:
            session = self.env['pos.session'].browse(session_id)
            if res_user.has_group('point_of_sale.group_pos_manager') or session.state in ('opened', 'closing_control'):
                vals['is_pos_manager'] = True
        return vals
