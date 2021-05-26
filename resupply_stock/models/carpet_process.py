from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
import time
import datetime

class internal_MenuForm(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _name='resupply.stock'
    _description="Stock ReSupply Request"
    _rec_name = 'get_id'
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approv','To be Approved'),
        ('in_progress','Waiting'),
        ('done', 'Done'),
        ('cancel','Rejected'),
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    
    def unlink(self):
        for leave in self:
            if leave.state in ('done'):
                raise UserError(_('You cannot delete an order form  which is not draft or cancelled. '))
            return super(internal_MenuForm, self).unlink()
  
    def resetdraft(self):
        self.write({'state':'cancel'})  
        
    def draft(self):
        if not self.product_line:
            raise UserError(_('Please add some product into lines'))
        self.write({'state':'in_progress'}) 
    
    def drafted(self):
        self.write({'state':'in_progress'}) 
        
    def drafts(self):
        self.write({'state':'done'}) 
        
    def reset(self):
        self.write({'state':'draft'}) 

    def _check_location_access(self, locations):
        loc_ids = []
        for location in locations:
            if location not in self.env.user.stock_location_ids.mapped('location_id').ids:
                loc_ids.append(location)
        if len(loc_ids):
            loc_list = self.env['stock.location'].browse(loc_ids).mapped('complete_name')
            raise UserError(_('You have no access for (%s) locations, Please contact system administrator!' % ', '.join(loc_list)))
        else:
            return True

    def button_validate(self):
        self._check_location_access([self.int_loc.id, self.dest_loc.id])
        if (self.int_loc and self.dest_loc):
            vals = {}
            for dgs in self.product_line:
                if not dgs.dest_loc.transit_loc:
                    raise UserError(_('Destinatin location has no transit location. Please assign it: %s') %dgs.dest_loc.name)
                pick_type_id = self.env['stock.picking.type'].search([('code','=','internal'), ('default_location_src_id','=', dgs.int_loc.id)], limit=1)
                if not pick_type_id:
                    raise UserError(_('Picking type not found. Please assign line requested from location in internal picking type'))
                key = (pick_type_id.id, dgs.int_loc.id, dgs.dest_loc.transit_loc.id)
                if vals.get(key):
                    vals[key].append({
                    'name':self.get_id,
                    'product_id': dgs.stock.id,
                    'product_uom_qty': dgs.qty,
                    'product_uom': dgs.stock.uom_id.id})
                else:
                    vals[key] = [{
                    'name': self.get_id,
                    'product_id': dgs.stock.id,
                    'product_uom_qty': dgs.qty,
                    'product_uom': dgs.stock.uom_id.id}]
        for key, move_vals in vals.items():
            pick_type_id, src_location, dest_loc = key
            # self._check_location_access([src_location, dest_loc])
            picking = self.env['stock.picking'].create({
                'location_id': src_location,
                'location_dest_id': dest_loc,
                'reference':self.get_id,
                'state': 'draft',
                'picking_type_id': pick_type_id,
                'move_lines': [(0, 0, m) for m in move_vals],
            })
            if picking:
                for move in picking.move_lines:
                    move.onchange_product_id()
                picking.action_confirm()
        self.write({'state':'done'})

    def _total_items(self):
        for request in self:
            request.total_items = len(request.product_line.mapped('stock'))

    total_items = fields.Integer('Total Items', compute='_total_items')
    product_line=fields.One2many("resupply.orderline","id_order")
    date_to=fields.Date("Start Date")
    date_from=fields.Date("End Date")
    logged_user=fields.Many2one('res.users','Requested BY',  default=lambda self: self.env.user)
    logged_user1=fields.Many2one('res.users','Approver')
    notes = fields.Text('Terms and Conditions')
    description= fields.Text('')
    get_id= fields.Char('Request Code', readonly=True, copy=False,)
    int_loc=fields.Many2one('stock.location',string="Requested From",  domain=[('usage', 'in', ['internal'])] )
    dest_loc=fields.Many2one('stock.location',string="Ship To",  domain=[('usage', 'in', ['internal'])] )
    is_request_readonly = fields.Boolean(compute='compute_is_request_readonly')
    stock_location_ids = fields.Many2many(
        'stock.location',
        compute='_compute_location_ids',
    )

    def _compute_location_ids(self):
        for request in self:
            if not self.env.user.stock_location_ids:
                request.stock_location_ids = self.env['stock.location'].search([]).ids  
            request.stock_location_ids = self.env.user.stock_location_ids.filtered(lambda x: x.is_default).mapped('location_id').ids

    @api.model
    def default_get(self, default_fields):
        res = super(internal_MenuForm, self).default_get(default_fields)
        user_loc_ids = self.env.user.stock_location_ids.filtered(lambda x: x.is_default).mapped('location_id').ids
        if user_loc_ids:        
            res.update({'stock_location_ids': user_loc_ids, 'dest_loc': user_loc_ids[0]})
        else:
            all_loc_ids = self.env['stock.location'].search([])
            res.update({'stock_location_ids': all_loc_ids.ids, 'dest_loc': all_loc_ids[0].id})
        return res

    def compute_is_request_readonly(self):
        for request in self:
            if request.state in ('cancel', 'done') or request.state in ('in_progress') and not self.env.user.has_group('resupply_stock.group_dysf_request_manager'):
                request.is_request_readonly = True
            else:
                request.is_request_readonly = False
   
    @api.model
    def create(self, vals):
        if 'get_id' not in vals or vals['get_id'] == False:
            sequence = self.env.ref('resupply_stock.get_id')
            vals['get_id'] = sequence.next_by_id()
        if vals.get('dest_loc') == vals.get('int_loc'):
            raise UserError(_('You cannot use same location !'))
        return super(internal_MenuForm, self).create(vals)

class internal_processLine_MenuForm(models.Model):
  
    _name='resupply.orderline'
    _description="ReSupply Stock order Form"
    
     
    id_order=fields.Many2one("resupply.stock")   
    stock=fields.Many2one("product.product","Product")
    description=fields.Char("Description")
    qty=fields.Float('Quantity', default=1.0)
    remarks=fields.Char("Notes") 
    date1=fields.Date('Requested Date')
    int_loc=fields.Many2one('stock.location',string="Requested From",domain=[('usage', 'in', ['internal'])])
    dest_loc=fields.Many2one('stock.location',string="Ship To",  domain=[('usage', 'in', ['internal'])] )

                
    @api.onchange('stock')
    def onchange_product_id(self):
        result = {}
        if not self.stock:
            return result
        product_lang = self.stock.with_context({
        })
        
        self.description = product_lang.display_name+ ' ' 
        if product_lang.description_purchase:
            self.description += '\n' + product_lang.description_purchase
        return result

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    reference = fields.Char(string="Request Reference")

    @api.model
    def create(self, vals):
        if vals.get('location_id') == vals.get('location_dest_id'):
            raise UserError(_('You cannot use same location !'))
        return super(StockPicking, self).create(vals)         

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_confirm(self, merge=True, merge_into=False):
        res = super(StockMove, self)._action_confirm(merge=merge, merge_into=merge_into)
        for final_move in res.move_dest_ids:
            if final_move.picking_id and res.picking_id:
                final_move.picking_id.reference = res.picking_id.reference
        return res