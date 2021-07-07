# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError



class MaterialReport(models.AbstractModel):
    _name = 'report.de_material_requirement_report.material_template'


    @api.model
    def _get_report_values(self, docids, data=None):

        model = self.env.context.get('active_model')
        act_id = self.env[model].browse(self.env.context.get('active_id'))

        for rec in act_id.activity_id:
            list = []
            records = self.env['material.requirement.data'].search([('activity_id', '=', act_id.id)])
            if records:
                for data in records:
                    list.append(data.product_id.id)
            for pro in rec.move_ids_without_package:
                if pro.product_id.id not in list:
                    vals = {
                        'activity_id': act_id.id,
                        'product_id': pro.product_id.id,
                        'quantity': pro.quantity_done,
                        'mr_demand': pro.product_uom_qty,
                        'mr_uom': pro.product_uom.id,
                        'mr_reserved': pro.reserved_availability
                    }
                    self.env['material.requirement.data'].create(vals)
                else:
                    quant = self.env['material.requirement.data'].search([('product_id', '=',pro.product_id.id),('activity_id', '=', act_id.id)])
                    quant.quantity = pro.quantity_done + quant.quantity
                    quant.mr_demand = pro.product_uom_qty + quant.mr_demand
                    quant.mr_reserved = pro.reserved_availability + quant.mr_reserved

        report_data = self.env['material.requirement.data'].search([('activity_id', '=', act_id.id)])

        return {
            'doc_model': 'material.requirement.data',
            'docs': report_data,
        }