# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InternalTransferReportWizard(models.TransientModel):
    _name = 'internal.transfer.report.wizard'
    _description = 'Internal Transfer report wizard'

    start_at = fields.Date(string='From Date', required=True)
    stop_at = fields.Date(string="To Date", required=True)
    location_id = fields.Many2one('stock.location', string="Source", domain="[('usage', 'in', ('internal', 'transit'))]")
    location_dest_id = fields.Many2one('stock.location', string="Destination", domain="[('usage', 'in', ('internal', 'transit'))]")
    state_ids = fields.Many2many('dxl.report.state', string='Status')
    category_ids = fields.Many2many('product.category', string='Product Category')

    def print_internal_transfer_report_xls(self):
        if self.start_at > self.stop_at:
            raise ValidationError(_('Invalid date !'))
        data = {
            'start_at': self.start_at,
            'stop_at': self.stop_at,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'state': self.state_ids.mapped('code'),
            'category_ids': self.category_ids.ids
        }
        return self.env.ref('dxl_internal_trasfer_report.int_trans_xlsx').report_action(self, data=data)
