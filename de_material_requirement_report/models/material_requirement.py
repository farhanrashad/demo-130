# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError



class MaterialRequirement(models.Model):
    _inherit = 'stock.picking'



    def open_wizard(self):

        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['stock.picking'].browse(selected_ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Material Requirement',
            'view_id': self.env.ref('de_material_requirement_report.open_wizard_form', False).id,
            'context': {'default_activity_id': selected_records.ids},
            'target': 'new',
            'res_model': 'material.requirement.wizard',
            'view_mode': 'form',
        }