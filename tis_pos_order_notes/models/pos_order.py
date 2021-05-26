# -*- coding: utf-8 -*-
# Copyright (C) 2019-Today  Technaureus Info Solutions(<http://technaureus.com/>).

from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    note = fields.Char(string='Note')


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)

        if ui_order.get('note', False):
            order_fields.update({
                'note': ui_order['note']
            })

        return order_fields
