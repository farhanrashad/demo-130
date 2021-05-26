# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    layer = env['stock.valuation.layer'].search([('product_id', '=', 25166)], limit=1)
    move_ids = [
        (286314, -1, 1307.0, -1307.0),
        (205925, -1, 1131.0, -1131.0),
        (205926, -1, 1131.0, -1131.0),
        (205927, -1, 1037.40, -1037.40)
    ]
    for move in move_ids:
        layer.copy({
            'stock_move_id': move[0],
            'quantity': move[1],
            'unit_cost': move[2],
            'value': move[2],
        })
    return True
