# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, AccessError, ValidationError


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    def action_mrp_bom_so(self):
        for record in self:
            if not record.order_line.bom_id:
                raise UserError(_('Bill of Material is require.'))
            else:
                for line in record.order_line:
                    self.env['mrp.production'].create({
                        'product_id': line.product_id.id,
                        'origin': record.name,
                        'product_qty': line.product_uom_qty,
                        'date_planned_start': fields.Date.today(),
                        'product_uom_id': line.product_id.uom_id.id,
                        'bom_id': line.bom_id.id,
                    })


class SaleOrderLineExt(models.Model):
    _inherit = 'sale.order.line'

    bom_id = fields.Many2one(comodel_name='mrp.bom', string='Bill of Material',
                             domain="[('product_tmpl_id.product_variant_ids','=',product_id)]"
                             )
