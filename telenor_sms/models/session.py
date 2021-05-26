# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SmsSession(models.Model):
    _name = "sms.session"
    _order = 'id desc'

    name = fields.Char('Session ID')
