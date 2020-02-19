# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning


from odoo.addons import decimal_precision as dp

class AccountApprovalLog(models.Model):
    _name = 'account.approval.log'
    _description = 'Account Approval Log'
    
    user_id = fields.Many2one('res.users', string='User', index=True, readonly=True, tracking=2, default=lambda self: self.env.user,)
    payment_id = fields.Many2one('account.payment',string='Payment No.',readonly=True)
    move_id = fields.Many2one('account.move',string='Account Move',readonly=True)
    status = fields.Char(string='Status',readonly=True)