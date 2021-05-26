# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class res_users(models.Model):
    _inherit = 'res.users'

    allow_mac_ids = fields.Many2many('user.allow.mac', 'user_mac_rel', 'user_id', 'allow_id', string='Allow Mac')
    mac_address_restrict = fields.Boolean(string='Mac Address Login Restriction', default=True)
          
                
class user_allow_mac(models.Model):
    _name = 'user.allow.mac'
    _description = 'User Allow Mac'

    name = fields.Char('Mac Address')
    allow_mac_ids = fields.Many2many('res.users', 'user_mac_rel', 'allow_id', 'user_id', string='Users')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
