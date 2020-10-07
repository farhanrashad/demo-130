# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class DisableNegativeStock(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        code = self.picking_type_id.code
        if code == 'incoming':
            purchase_order = self.env['purchase.order'].search([('name', '=', self.origin)])
            for line in purchase_order.order_line:
                print('line', line)
                tmpl_id = line.product_id.product_tmpl_id.id
                print('tmpl', tmpl_id)
                bom_obj = self.env['mrp.bom'].search([('product_tmpl_id', '=', tmpl_id)])
                print('bom_obj', bom_obj)
                for bom in bom_obj:
                    if bom.type == 'subcontract':
                        delivery_orders = self.env['stock.picking'].search([('origin', '=', self.name)])
                        for order in delivery_orders:
                            if order.state != 'done':
                                raise UserError(_('Please make sure you have sent the required '
                                                  'products to your subcontractor.'))
                            else:
                                return super(DisableNegativeStock, self).button_validate()
                    else:
                        return super(DisableNegativeStock, self).button_validate()
        else:
            return super(DisableNegativeStock, self).button_validate()
