# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskExtendInherit(models.Model):
    _inherit = 'helpdesk.ticket.team'
    _description = 'This table handle the data of helpdesk'

    technician_ids = fields.Many2one('res.users', string='Technician')


class HelpdeskExtends(models.Model):
    _inherit = 'helpdesk.ticket'
    _description = 'This table handle the data of helpdesk tickets'

    technician_id = fields.Many2one('res.users',string='Technician')