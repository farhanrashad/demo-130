# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions(<http://technaureus.com/>).

from odoo import models, fields, api
from odoo.tools import float_compare

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _validate_session(self):
        self.ensure_one()
        self._check_if_no_draft_orders()
        # Users without any accounting rights won't be able to create the journal entry. If this
        # case, switch to sudo for creation and posting.
        sudo = False
        if (
            not self.env['account.move'].check_access_rights('create', raise_exception=False)
            and self.user_has_groups('point_of_sale.group_pos_user')
        ):
            sudo = True
            self.sudo()._create_account_move()
        else:
            self.sudo()._create_account_move()
        if self.move_id.line_ids:
            self.move_id.sudo().post() if not sudo else self.move_id.sudo().post()
            # Set the uninvoiced orders' state to 'done'
            self.env['pos.order'].search([('session_id', '=', self.id), ('state', '=', 'paid')]).write({'state': 'done'})
        else:
            # The cash register needs to be confirmed for cash diffs
            # made thru cash in/out when sesion is in cash_control.
            if self.config_id.cash_control:
                self.cash_register_id.button_confirm_bank()
            self.move_id.sudo().unlink()
        self.write({'state': 'closed'})
        return {
            'type': 'ir.actions.client',
            'name': 'Point of Sale Menu',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('point_of_sale.menu_point_root').id},
        }
