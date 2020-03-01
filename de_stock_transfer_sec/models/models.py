# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Stockwarehouse(models.Model):
    _name = 'stock.warehouse.transfer'
    _description = 'this is warehouse transfer model'
    _rec_name = 'name_seq'

    def action_validate(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validate'}, context=context)
        return True

    def action_draft(self):
        for i in self:
            i.write({'state': 'draft'})

    def action_validate(self):
        for i in self:
            i.write({'state': 'validate'})

    def action_transfer_in(self):
        for i in self:
            i.write({'state': 'transfer_in'})

    def action_transfer_out(self):
        for i in self:
            i.write({'state': 'transfer_out'})

    def action_done(self):
        for i in self:
            i.write({'state': 'done'})

    def stock_transfer(self):
        return {
            'name': '_(stocktransfer)',
            'domain': [],
            'view_type': 'form',
            'res_model': 'stock.warehouse.transfer',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
    def action_picking(self):
        return {
            'name': '_(stock)',
            'domain': [],
            'view_type': 'wizard',
            'res_model': 'picking.picking',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }


    transfer_date = fields.Date(string='Transfer Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.partner', string='User Name')
    test_id = fields.Char(string='text', states={'validate': [('readonly', True)]})
    stock_reference = fields.One2many('stock.warehouse.transfer.line', 'stock_transfer_line')
    from_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse From')
    to_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse To')
    from_location_id = fields.Many2one('stock.warehouse', string='Location From')
    to_location_id = fields.Many2one('stock.warehouse', string='Location To')
    picking_ids_is = fields.Many2one('stock.warehouse.transfer', string='Picking Documents')
    name_seq = fields.Char(string="Order Reference", required=True, readonly=True, copy=False, index=True,
                           default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ('transfer_in', 'Transfer in'),
        ('transfer_out', 'Transfer out'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, index=True, select=True, tracking=3, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('stock.warehouse.transfer.sequence') or _('New')
        result = super(Stockwarehouse, self).create(vals)
        return result


class Stocktransferline(models.Model):
    _name = 'stock.warehouse.transfer.line'
    _description = 'this is line model'

    # def set_defaupt_val(self):
    #     for i in self:
    #         i.transfer_in_quantity = i.quantity

    Product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Char(string='Product id', related='Product_id.default_code')
    quantity = fields.Float(string='Quantity')
    transfer_out_quantity = fields.Float(string='Transfer out quantity', compute='_compute_quantity_out',
                                         inverse='_inverse_quantity_out', store=True,
                                         )

    transfer_in_quantity = fields.Float(string='Transfer in quantity', compute='_compute_quantity',
                                        inverse='_inverse_quantity',
                                        store=True)
    stock_transfer_line = fields.Many2one('stock.warehouse.transfer', string='reference')

    @api.depends('quantity')
    def _compute_quantity_out(self):
        for i in self:
            i.transfer_out_quantity = i.quantity

    @api.depends('transfer_out_quantity')
    def _inverse_quantity_out(self):
        for i in self:
            i.transfer_out_quantity = i.transfer_out_quantity

    @api.depends('quantity')
    def _compute_quantity(self):
        for i in self:
            i.transfer_in_quantity = i.quantity

    @api.depends('transfer_in_quantity')
    def _inverse_quantity(self):
        for i in self:
            i.transfer_in_quantity = i.transfer_in_quantity


class Stockpickling(models.Model):
    _inherit = 'stock.picking'

    stock_transfer_id = fields.Many2one('stock.warehouse.transfer', string='Stock Transfer Reference')
