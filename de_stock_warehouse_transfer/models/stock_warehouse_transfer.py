# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Stockwarehouse(models.Model):
    _name = 'stock.warehouse.transfer'
    _description = 'this is warehouse transfer model'
    _rec_name = 'name_seq'

    def get_picking_out_count(self):
        count = self.env['stock.picking'].search_count([])
        self.picking_out = count

    def action_validate(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'validate'}, context=context)
        return True

    def action_draft(self):
        for rs in self:
            rs.write({'state': 'draft'})

    def action_validate(self):
        for rs in self:
            rs.write({'state': 'validate'})

    def action_transfer_in(self):
        picking_incoming = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
        vals = {
            'location_id': self.from_location_id.id,
            'location_dest_id': self.to_location_id.id,
            # 'stock_move_id': self.stock_move_id,
            'picking_type_id': picking_incoming.id,
            'warehouse_trasnfer_id': self.id,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.stock_transfer_lines:
            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Transfer Out',
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.id,
                'location_dest_id': line.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                'quantity_done': line.transfer_in_quantity,
            }
            stock_move = self.env['stock.move'].create(lines)

            moves = {
                'move_id': stock_move.id,
                'product_id': line.product_id.id,
                # 'product_uom': line.product_id.uom_id.id,
                'location_id': line.id,
                'location_dest_id': line.id,
                # 'company_id': mv.id,
                # 'date': line.date,
                # 'lot_id':line.batch_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'product_uom_qty': line.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                # 'quantity_done': mv.id,
            }
            stock_move_line_id = self.env['stock.move.line'].create(moves)

        # for rs in self:
        #     rs.write({'state': 'transfer_in'})


    def action_transfer_out(self):
        picking_outgoing = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
        vals = {
            'location_id': self.from_location_id.id,
            'location_dest_id': self.to_location_id.id,
            # 'stock_move_id': self.stock_move_id,
            'picking_type_id': picking_outgoing.id,
            'warehouse_trasnfer_id': self.id,
        }
        picking = self.env['stock.picking'].create(vals)
        for line in self.stock_transfer_lines:
            lines = {
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'name': 'Transfer Out',
                'product_uom': line.product_id.uom_id.id,
                'location_id': line.id,
                'location_dest_id': line.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                'quantity_done': line.transfer_out_quantity,
            }
            stock_move=self.env['stock.move'].create(lines)

            moves = {
                'move_id': stock_move.id,
                'product_id': line.product_id.id,
                # 'product_uom': line.product_id.uom_id.id,
                'location_id': line.id,
                'location_dest_id': line.id,
                #'company_id': mv.id,
                # 'date': line.date,
                # 'lot_id':line.batch_id.id,
                'product_uom_id': line.product_id.uom_id.id,
                'product_uom_qty': line.id,
                # 'bom_id': line.bom_id.id,
                # 'product_uom_qty': line.product_uom_id,
                # 'quantity_done': mv.id,
            }
            stock_move_line_id = self.env['stock.move.line'].create(moves)


        # for rs in self:
        #     rs.write({'state': 'transfer_out'})

    def action_done(self):
        for rs in self:
            rs.write({'state': 'done'})

    # def stock_transfer(self):
    #     return {
    #         'name': '_(stocktransfer)',
    #         'domain': [],
    #         'view_type': 'form',
    #
    #         'res_model': 'stock.warehouse.transfer',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'type': 'ir.actions.act_window'
    #     }

    # def internal_picking(self):
    #     return {
    #         'name': '_(picking)',
    #         'domain': [],
    #         'view_type': 'form',
    #         'res_model': 'stock.picking',
    #         'view_id': False,
    #         'view_mode': 'tree,form',
    #         'type': 'ir.actions.act_window'
    #     }

    # def _get_stock_type_ids(self):
    #     data = self.env['stock.picking.type'].search([])
    #
    #     if self._context.get('default_type') == 'outgoing':
    #         for line in data:
    #             if line.code == 'outgoing':
    #                 return line
    #     if self._context.get('default_type') == 'incoming':
    #         for line in data:
    #             if line.code == 'incoming':
    #                 return line
    picking_out = fields.Integer(compute='get_picking_out_count')

    transfer_date = fields.Date(string='Transfer Date', default=fields.Datetime.now)
    user_id = fields.Many2one(
        'res.users', 'Responsible', tracking=True,
        domain=lambda self: [('groups_id', 'in', self.env.ref('stock.group_stock_user').id)],
        # states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        default=lambda self: self.env.user)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda s: s.env.company.id, index=True, states={'validate': [('readonly', True)]})
    stock_transfer_lines = fields.One2many('stock.warehouse.transfer.line', 'stock_transfer_id',
                                     string='Stock Transfer Lines',
                                     # states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
                                     auto_join=True)

    from_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse From')
    to_warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse To')
    from_location_id = fields.Many2one('stock.location', string='Location From')
    to_location_id = fields.Many2one('stock.location', string='Location To')
    # picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',
    #                                   default=_get_stock_type_ids,
    #                                   help="This will determine picking type of incoming shipment")
    # # bom_ids = fields.One2many('stock.bom', 'product_tmpl_id', string='Bill of Materials')
    # bom_count = fields.Integer(string='BOMs', compute='_compute_bom_ids')

    picking_ids = fields.One2many('stock.picking', 'warehouse_trasnfer_id', string='Pickings')
    picking_count = fields.Integer(string='Pickings', compute='_compute_picking_count')

    name_seq = fields.Char(string="Order Reference", required=True, readonly=True, copy=False, index=True,
                           default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ('transfer_in', 'Transfer in'),
        ('transfer_out', 'Transfer out'),
        ('done', 'Done'),
    ], string='Status', readonly=True, copy=False, index=True, select=True, tracking=3, default='draft')

    @api.depends('picking_ids')
    def _compute_picking_count(self):
        picking_data = self.env['stock.picking'].sudo().read_group([('warehouse_trasnfer_id', 'in', self.ids)],
                                                                   ['warehouse_trasnfer_id'], ['warehouse_trasnfer_id'])
        mapped_data = dict([(r['warehouse_trasnfer_id'][0], r['picking_count']) for r in picking_data])
        for picking in self:
            picking.picking_count = mapped_data.get(picking.id, 0)

    def action_view_picking(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Picking'),
            'res_model': 'stock.picking',
            'view_mode': 'tree,form',
            'domain': [('warehouse_trasnfer_id', '=', self.id)],
            'context': dict(self._context, create=False, default_company_id=self.company_id.id,
                            default_warehouse_transfer_id=self.id),
        }

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('stock.warehouse.transfer.sequence') or _('New')
        result = super(Stockwarehouse, self).create(vals)
        return result

    # @api.depends('bom_ids')
    # def _compute_bom_ids(self):
    #     b = 0
    #     for order in self:
    #         for line in order.stock_transfer_lines:
    #             b = len(line.product_tmpl_id.bom_ids)
    #         order.bom_count = b
    #
    # def action_view_bom(self):
    #     action = self.env.ref('stock.stock_bom_tree_view').read()[0]
    #
    #     boms = self.mapped('boms_ids')
    #     if len(boms) > 1:
    #         action['domain'] = [('id', 'in', boms.ids)]
    #     elif boms:
    #         action['views'] = [(self.env.ref('stock.stock_bom_form_view').id, 'form')]
    #         action['res_id'] = boms.id
    #     return action


class Stocktransferline(models.Model):
    _name = 'stock.warehouse.transfer.line'
    _description = 'this is line model'

    # def set_defaupt_val(self):
    #     for i in self:
    #         i.transfer_in_quantity = i.quantity

    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Char(string='Product id',     related='product_id.default_code')
    #, related='Product_id.default_code
    quantity = fields.Float(string='Quantity')
    transfer_out_quantity = fields.Float(string='Transfer out quantity', compute='_compute_quantity_out',
                                         inverse='_inverse_quantity_out', store=True,
                                         )

    transfer_in_quantity = fields.Float(string='Transfer in quantity', compute='_compute_quantity',
                                        inverse='_inverse_quantity',
                                        store=True)

    stock_transfer_id = fields.Many2one('stock.warehouse.transfer', string='Transfer Order', index=True, required=True,
                                        ondelete='cascade')

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
