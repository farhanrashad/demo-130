# -*- coding: utf-8 -*-
# Copyright (C) 2019-present  Technaureus Info Solutions(<http://www.technaureus.com/>).
from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)


class pos_config(models.Model):
    _inherit = "pos.config"

    order_note = fields.Boolean(string='Order Note', default=1)
    orderline_note = fields.Boolean(string='Order Line Note', default=1)
    print_notes = fields.Boolean(string='Print Notes on Receipt', default=1)
