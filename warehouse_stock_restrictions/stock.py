# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_locations = fields.Boolean('Restrict Location')

    # stock_location_ids = fields.Many2many(
    #     'stock.location',
    #     'location_security_stock_location_users',
    #     'user_id',
    #     'location_id',
    #     'Stock Locations')
    stock_location_ids = fields.One2many('user.location', 'user_id')

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Warehouse Operations')

    @api.onchange('restrict_locations')
    def _onchange_rewrite_options(self):
        for user in self:
            if not user.restrict_locations:
                user.stock_location_ids = False

class UserLocation(models.Model):
    _name = 'user.location'

    is_default = fields.Boolean('Is Default')
    user_id = fields.Many2one('res.users')
    location_id = fields.Many2one('stock.location', string='Location')


# class stock_move(models.Model):
#     _inherit = 'stock.move'

#     @api.constrains('state', 'location_id', 'location_dest_id')
#     def check_user_location_rights(self):
#         for rec in self:
#             if rec.state == 'draft':
#                 return True
#             user_locations = self.env.user.stock_location_ids
#             if self.env.user.restrict_locations:
#                 message = _(
#                     'Invalid Location. You cannot process this move since you do '
#                     'not control the location "%s". '
#                     'Please contact your Adminstrator.')
#                 if rec.location_id not in user_locations:
#                     raise Warning(message % rec.location_id.name)
#                 elif rec.location_dest_id not in user_locations:
#                     raise Warning(message % rec.location_dest_id.name)


class Product(models.Model):
    _inherit = 'product.product'


    def _get_domain_locations(self):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = super(Product, self)._get_domain_locations()
        user_location_ids = self.env.user.stock_location_ids.ids
        if len(user_location_ids):
            domain_quant_loc += [
                '|', ('location_id', 'in', user_location_ids),
                ('location_id', 'child_of', user_location_ids)
            ]
        return domain_quant_loc, domain_move_in_loc, domain_move_out_loc

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def check_picking_user_location_rights(self, location_id):
        loc_ids = []
        if not self.env.user.has_group('stock.group_stock_manager') and location_id and location_id not in self.env.user.stock_location_ids.mapped('location_id').ids:
            location = self.env['stock.location'].browse(location_id)
            raise UserError(_('You have no access for (%s) locations, Please contact system administrator!' % location.complete_name))

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('stock.group_stock_manager'):
            self.check_picking_user_location_rights(vals.get('location_id'))
        return super(StockPicking, self).create(vals)

    def write(self, vals):
        if not self.env.user.has_group('stock.group_stock_manager'):
            self.check_picking_user_location_rights(vals.get('location_id'))
        return super(StockPicking, self).write(vals)
