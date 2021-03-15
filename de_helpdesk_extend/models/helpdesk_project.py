# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    domestic_cash = fields.Text()
