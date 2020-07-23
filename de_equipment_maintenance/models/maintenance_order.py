# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError, AccessError
from collections import defaultdict


class StockPickingExt(models.Model):
    _inherit = 'stock.picking'

    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_src_id,
        check_company=True, readonly=True, required=False,
        states={'draft': [('readonly', False)]})
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=lambda self: self.env['stock.picking.type'].browse(
            self._context.get('default_picking_type_id')).default_location_dest_id,
        check_company=True, readonly=True, required=False,
        states={'draft': [('readonly', False)]})
    requisition_po_id = fields.Many2one(comodel_name='maintenance.order', string='Purchase Requisition')


class StockMoveExt(models.Model):
    _inherit = 'stock.move'

    de_quantity_done = fields.Float(string='Done')


class MaintenanceOrder(models.Model):
    _name = 'maintenance.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maintenance Order'
    _order = 'id desc'

    @api.model
    def _get_default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            (
                'warehouse_id.company_id', 'in',
                [self.env.context.get('company_id', self.env.user.company_id.id), False])],
            limit=1).id

    @api.depends('maintenance_part_ids.unit_cost', 'maintenance_part_ids.product_uom_qty',
                 'maintenance_part_ids.product_id',
                 'maintenance_service_ids.product_id', 'maintenance_service_ids.product_uom_qty',
                 'maintenance_service_ids.product_cost')
    def _cost_all(self):
        self.ensure_one()
        val = 0.0
        for part in self.maintenance_part_ids:
            val = val + (part.product_uom_qty * part.unit_cost)
        for service in self.maintenance_service_ids:
            val = val + (service.product_uom_qty * service.product_cost)
        self.cost_total = val

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    def action_view_delivery(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_id=picking_id.id,
                                 default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.ref,
                                 default_group_id=picking_id.group_id.id)
        return action

    @api.model
    def create(self, values):
        seq = self.env['ir.sequence'].get('maintenance.order')
        values['name'] = seq
        res = super(MaintenanceOrder, self).create(values)
        return res

    def action_confirm(self):
        stock_picking_obj = self.env['stock.picking']
        stock_picking_line_obj = self.env['stock.move']
        for line in self.maintenance_lines:
            pur_order = stock_picking_obj.search(
                [('requisition_po_id', '=', self.id)])
            if pur_order:
                supplier_line = {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.demand_qty,
                    'product_uom': line.product_uom.id,
                    'location_id': self.location_src_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'name': self.name,
                    'picking_id': pur_order.id,
                    'emm_order_id': self.id,
                    # 'quantity_done': self.move_lines.product_uom_qty,
                }
                purchase_order_line = stock_picking_line_obj.create(supplier_line)
            else:
                vals = {
                    'picking_type_id': self.picking_type_id.id,
                    'location_id': self.location_src_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'origin': self.name,
                    'requisition_po_id': self.id,
                }
                stock_picking = stock_picking_obj.create(vals)
                po_line_vals = {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.demand_qty,
                    'product_uom': line.product_uom.id,
                    'location_id': self.location_src_id.id,
                    'location_dest_id': self.location_dest_id.id,
                    'name': self.name,
                    'picking_id': stock_picking.id,
                    'emm_order_id': self.id,
                    # 'quantity_done': self.move_lines.product_uom_qty,
                }
                stock_lines = stock_picking_line_obj.create(po_line_vals)
        res = self.write({
            'state': 'confirm',
            'date_order': fields.Datetime.now()
        })
        return res
    # def action_confirm(self):
    #     self.write({
    #         'state': 'confirm',
    #         'date_order': fields.Datetime.now()
    #     })
    #     supplier_line = {
    #         'product_id': self.move_lines.product_id.id,
    #         'product_uom_qty': self.move_lines.product_uom_qty,
    #         'product_uom': self.move_lines.product_uom.id,
    #         'location_id': self.location_src_id.id,
    #         'location_dest_id': self.location_dest_id.id,
    #         'name': self.name,
    #         # 'quantity_done': self.move_lines.product_uom_qty,
    #     }
    #     record_line = {
    #         'picking_type_id': self.picking_type_id.id,
    #         'location_id': self.location_src_id.id,
    #         'location_dest_id': self.location_dest_id.id,
    #         'origin': self.name,
    #         'move_ids_without_package': [(0, 0, supplier_line)],
    #     }
    #     record = self.env['stock.picking'].create(record_line)
    #     return record

    def action_cancel(self):
        self.write({'state': 'cancel'})
        ex_picking = self.env['stock.picking'].search([('origin', '=', self.name)])
        if ex_picking:
            ex_picking.state = 'cancel'

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_start_maintenance(self):
        maintenance_lines = self.env['maintenance.order.line'].search([('maintenance_line', '=', self.id)])
        print('maintenance_lines', maintenance_lines)
        location = self.env['stock.location'].search([('id', '=', self.location_src_id.id)])
        quant_obj = self.env['stock.quant']
        for sm in maintenance_lines:
            qty_available = quant_obj._get_available_quantity(sm.product_id, location)
            print('qty', qty_available)
            if sm.demand_qty > qty_available:
                raise ValidationError(_("Quantity is not available at current location for " + str(sm.product_id.name)))
            else:
                # ex_lines = self.env['stock.picking'].search([('origin', '=', self.name)])
                # moves = self.env['stock.move'].search([('picking_id', '=', ex_lines.id)])
                # for m in moves:
                #     m.quantity_done = m.product_uom_qty
                ex_location = quant_obj.search([('location_id', '=', location.id),
                                                ('product_id', '=', sm.product_id.id)])
                quantity = ex_location.quantity - sm.demand_qty
                new_quantity = (sm.demand_qty) * -1
                # self.env['stock.quant']._update_available_quantity(sm.product_id, location, new_quantity)
        self.write({
            'state': 'inprocess',
            'start_date': fields.Datetime.now()
        })
        for move in self.maintenance_lines:
            move.update({
                'done_qty': move.demand_qty,
                'reserved_qty': move.demand_qty,
                    # 'reserved_availability': move.product_uom_qty,
                    # 'quantity_done': move.product_uom_qty,
                # 'state': 'done'
            })
        ex_lines = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        moves = self.env['stock.move'].search([('picking_id', '=', ex_lines.id)])
        for move in moves:
            move.update({
                'reserved_availability': move.product_uom_qty,
                'quantity_done': move.product_uom_qty,
            })
            # move.reserved_availability = move.product_uom_qty
            # move.quantity_done = move.product_uom_qty
        # moves.quantity_done = self.move_lines.de_quantity_done
        # return record

    def action_end_maintenance(self):
        stock_moves = self.env['maintenance.order.line'].search([('maintenance_line', '=', self.id)])
        location = self.env['stock.location'].search([('id', '=', self.location_src_id.id)])
        quant_obj = self.env['stock.quant']
        for m in stock_moves:
            ex_location = quant_obj.search([('location_id', '=', location.id),
                                            ('product_id', '=', m.product_id.id)])
            quantity = ex_location.quantity - m.demand_qty
            new_quantity = (m.demand_qty) * -1
            # self.env['stock.quant']._update_available_quantity(m.product_id, location, new_quantity)
        ex_lines = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        moves = self.env['stock.move.line'].search([('reference', '=', ex_lines.name)])
        for mv in moves:
            mv.update({
                'state': 'done'
            })
        # self.env['stock.move.line'].create({
        #     'date': fields.Date.today(),
        #     'reference': self.name,
        #     'product_id': stock_moves.product_id.id,
        #     'location_id': self.location_src_id.id,
        #     'location_dest_id': self.location_dest_id.id,
        #     'qty_done': stock_moves.product_uom_qty,
        #     'product_uom_id': stock_moves.product_uom.id,
        # })
        ex_pick_doc = self.env['stock.picking'].search([('origin', '=', self.name)])
        for ex in ex_pick_doc:
            ex.state = 'done'
        self.write({
            'state': 'done',
            'end_date': fields.Datetime.now()
        })
        ex_lines = self.env['stock.picking'].search([('origin', '=', self.name)], limit=1)
        # ex_lines.action_confirm()
        # ex_lines.action_assign()
        # ex_lines.button_validate()
        # self.env['stock.move.line'].create({
        #     'date': fields.Date.today(),
        #     'reference': self.name,
        #     'product_id': self.move_lines.product_id.id,
        #     'location_id': self.location_src_id.id,
        #     'location_dest_id': self.location_dest_id.id,
        #     'qty_done': self.move_lines.product_uom_qty,
        #     'company_id': self.env.user.company_id.id,
        #     'product_uom_id': self.move_lines.product_uom.id,
        #     'state': 'done',
        # })

    def action_create_delivery(self):
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
        stock_location = warehouse.lot_stock_id
        vals = {
            'move_type': 'one',
            'scheduled_date': fields.Datetime.now(),
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_src_id.id,
            'location_dest_id': self.location_dest_id.id,
            'em_order_id': self.id,
        }
        picking_id = self.env['stock.picking'].create(vals)
        for line in self.maintenance_part_ids:
            vals = {
                'company_id': self.company_id.id,
                'name': self.name,
                'date': fields.Datetime.now(),
                'date_expected': fields.Datetime.now(),
                'location_id': self.location_src_id.id,
                'location_dest_id': self.location_dest_id.id,
                'picking_id': picking_id.id,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'product_uom_qty': line.product_uom_qty,

            }
            move_id = self.env['stock.move'].create(vals)

    def action_create_bill(self):
        vals = {
            'test': 1,
        }
        for line in self.maintenance_service_ids:
            vals = {
                'test': 1,
            }

    @api.onchange('picking_type_id')
    def _onchange_picking_type(self):
        for rec in self:
            rec.location_src_id = rec.picking_type_id.default_location_src_id.id
            rec.location_dest_id = rec.picking_type_id.default_location_dest_id.id

    maintenance_request_id = fields.Many2one('maintenance.request', string="Maintenance Request",
                                             help="Related Maintenance Request")
    equipment_id = fields.Many2one('maintenance.equipment', string='Equipment', required=True, readonly=True,
                                   states={'draft': [('readonly', False)]},
                                   ondelete='restrict', index=True, check_company=True)
    name = fields.Char(string='Order Reference', copy=False, readonly=True, index=True, default=lambda self: _('New'))
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, default=fields.Datetime.now,
                                 states={'draft': [('readonly', False)]})
    date_confirmed = fields.Date(string='Confirmation Date', required=False, readonly=True, )
    schedule_start_date = fields.Date(string='Schedule Start Date', required=False, readonly=True,
                                      states={'draft': [('readonly', False)]}, )
    schedule_end_date = fields.Date(string='Schedule End Date', required=False, readonly=True,
                                    states={'draft': [('readonly', False)]}, )

    start_date = fields.Date(string='Start Date', required=False, readonly=True, )
    end_date = fields.Date(string='End Date', required=False, readonly=True, )

    date_closed = fields.Date(string='Closed Date', required=False, readonly=True, )

    pfiled = fields.Many2one(comodel_name="maintenance.equipment", related='equipment_id.equipment_id',
                             string="Parent Equipment", required=False)
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('repair.order'))
    maintenance_team_id = fields.Many2one('maintenance.team', string='Maintenance Team')
    user_id = fields.Many2one('res.users', string='Responsible', index=True, tracking=2,
                              default=lambda self: self.env.user, domain=lambda self: [
            ('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True,
                                          states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                          help="The analytic account related to a sales order.", copy=False,
                                          oldname='project_id')
    description = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('inprocess', 'Under Maintenance'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')], string="Status", default='draft', track_visibility='onchange')

    maintenance_part_ids = fields.One2many('maintenance.order.part.lines', 'em_order_id', string='Maintenance Lines',
                                           copy=True, auto_join=True, readonly=True,
                                           states={'draft': [('readonly', False)]})

    move_lines = fields.One2many('stock.move', 'emm_order_id', string="Maintenance Stock Moves", copy=True,
                                 readonly=True, states={'draft': [('readonly', False)]})
    maintenance_lines = fields.One2many(comodel_name='maintenance.order.line', inverse_name='maintenance_line')

    maintenance_service_ids = fields.One2many('maintenance.order.service.lines', 'em_order_id',
                                              string='Maintenance Service Lines', copy=True, auto_join=True,
                                              readonly=True, states={'draft': [('readonly', False)]})

    cost_total = fields.Float(string='Total Cost', store=True, readonly=True, compute='_cost_all',
                              track_visibility='always', track_sequence=6)

    picking_ids = fields.One2many('stock.picking', 'em_order_id', string='Transfers')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        default=_get_default_picking_type, required=True)
    location_src_id = fields.Many2one(
        'stock.location', 'Raw Materials Location',
        readonly=True, required=True,
        states={'confirmed': [('readonly', False)]},
        help="Location where the system will look for components.")
    location_dest_id = fields.Many2one(
        'stock.location', 'Finished Products Location',
        readonly=True, required=True,
        states={'confirmed': [('readonly', False)]},
        help="Location where the system will stock the finished products.")

    partner_id = fields.Many2one(comodel_name='res.partner', string='Origen del Consolidado')


class MaintenanceParts(models.Model):
    _name = 'maintenance.order.part.lines'
    _description = "Maintenance Part Lines"

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True,
                                  ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True,
                                 domain="[('type', 'in', ['product', 'consu'])]")
    product_uom_qty = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'),
                                   default=1.0)
    product_uom_id = fields.Many2one('uom.uom', required=True, string='Unit of Measure', change_default=True,
                                     default=_get_default_product_uom_id)
    product_uom_category_id = fields.Many2one(comodel_name='uom.category', related='product_id.uom_id.category_id')
    unit_cost = fields.Float(string='Unit cost', compute='_get_unit_cost')
    total_cost = fields.Float(string='Total Cost', compute='_get_total_cost')
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        index=True, required=True)
    location_dest_id = fields.Many2one(
        'stock.location', 'Dest. Location',
        index=True, required=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        """ On change of operation type it sets source location, destination location
        and to invoice field.
        @param product: Changed operation type.
        @param guarantee_limit: Guarantee limit of current record.
        @return: Dictionary of values.
        """
        args = self.em_order_id.company_id and [('company_id', '=', self.em_order_id.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        self.location_id = warehouse.lot_stock_id
        self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        self.product_uom_id = self.product_id.uom_id.id

    @api.depends('product_id')
    def _get_unit_cost(self):
        """ Returns the unit price to store on the quant """
        for rs in self:
            unit_price = rs.product_id.standard_price
            rs.update({
                'unit_cost': unit_price
            })

    @api.depends('product_id', 'product_uom_qty', 'unit_cost')
    def _get_total_cost(self):
        for rs in self:
            rs.update({
                'total_cost': rs.unit_cost * rs.product_uom_qty
            })

    def _calculate_unit_price(self):
        return 0


class MaintenanceOperations(models.Model):
    _name = 'maintenance.order.service.lines'
    _description = "Maintenance Service Lines"

    def _get_default_product_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    @api.depends('product_id')
    def _compute_service_cost(self):
        return self.product_id.standard_price

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.product_uom_id = self.product_id.uom_id.id
        self.product_cost = self.product_id.standard_price * self.product_uom_qty

    em_order_id = fields.Many2one('maintenance.order', string='Order Reference', index=True, required=True,
                                  ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True,
                                 domain="[('type', 'not in', ['product', 'consu'])]", )
    product_uom_qty = fields.Float(string='Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'),
                                   default=1.0)
    product_uom_id = fields.Many2one('uom.uom', required=True, string='Unit of Measure', change_default=True,
                                     default=_get_default_product_uom_id)
    product_uom_category_id = fields.Many2one(comodel_name='uom.category', related='product_id.uom_id.category_id')
    product_cost = fields.Float(string='Cost')
    has_tracking = fields.Selection(related='product_id.tracking', string='Product with Tracking', readonly=True)
    picking_id = fields.Many2one('stock.picking', 'Transfer Reference', index=True)


class MaintenanceOrderLine(models.Model):
    _name = 'maintenance.order.line'
    _description = 'Maintenance Lines'

    maintenance_line = fields.Many2one(comodel_name='maintenance.order')
    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
    demand_qty = fields.Float(string='Initial Demand')
    reserved_qty = fields.Float(string='Reserved Quantity', readonly=True)
    done_qty = fields.Float(string='Done', readonly=True)
    product_uom = fields.Many2one(comodel_name='uom.uom', string='Unit of Measure', required=True,
                                  related='product_id.uom_id')

