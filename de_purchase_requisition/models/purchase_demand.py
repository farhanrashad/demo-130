# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class PurchaseDemand(models.Model):
    _name = 'purchase.demand'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Purchase Demand'
    _order = 'date_requisition desc, id desc'
    _check_company_auto = True
    
    
    user_id = fields.Many2one('res.users', string="Request Owner",check_company=True, domain="[('company_ids', 'in', company_id)]", default=lambda self: self.env.user, required=True,readonly=True, states={'draft': [('readonly', False)]},)
    employee_id = fields.Many2one('hr.employee', string='Employee', related="user_id.employee_id")
    department_id = fields.Many2one('hr.department', string='Department',related="employee_id.department_id")
    
    demand_type_id = fields.Many2one('purchase.demand.type', string='Requisition Type', index=True, required=True, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'New'),
        ('in_progress', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=4, default='draft')
    date_requisition = fields.Datetime(string='Requisition Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Creation date of draft requisition.")
    date_deadline = fields.Datetime(string='Requisition Deadline', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Deadline date of requisition.")
    schedule_date = fields.Date(string='Delivery Date', index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, help="The expected and scheduled delivery date where all the products are received", tracking=True)
    purchase_demand_line = fields.One2many('purchase.demand.line', 'purchase_demand_id', string='Requisition Line', copy=True, auto_join=True,readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    description = fields.Text()
    order_count = fields.Integer(compute='_compute_orders_number', string='Number of Orders')
    purchase_ids = fields.One2many('purchase.order', 'purchase_demand_id', string='Purchase Orders', states={'done': [('readonly', True)]})
    
    
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'date_requisition' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_requisition']))
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.requisition', sequence_date=seq_date) or _('New')
        result = super(PurchaseDemand, self).create(vals)
        return result
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_confirm(self):
        self.state = 'in_progress'
        
    def action_done(self):
        """
        Generate all purchase order based on selected lines, should only be called on one agreement at a time
        """
        if any(purchase_order.state in ['draft', 'sent', 'to approve'] for purchase_order in self.mapped('purchase_ids')):
            raise UserError(_('You have to cancel or validate every RfQ before closing the purchase requisition.'))
        self.write({'state': 'done'})
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def unlink(self):
        if any(requisition.state not in ('draft', 'cancel') for requisition in self):
            raise UserError(_('You can only delete draft requisitions.'))
        # Draft requisitions could have some requisition lines.
        self.mapped('purchase_demand_line').unlink()
        return super(PurchaseDemand, self).unlink()
        
    def action_purchase_transfer(self):
        pvals = moves = move_lines = {}
        purchase_id = self.env['purchase.order']
        purchase_line_id = self.env['purchase.order.line']
        
        for demand in self: #generate purchase order and internal transfer documents
            for line in demand.purchase_demand_line:
                if line.demand_action == 'purchase':
                    if line.partner_id:
                        purchase_id = self.env['purchase.order'].search([('partner_id','=',line.partner_id.id),('state','=','draft')])
                        if not purchase_id:
                            purchase_id = self.env['purchase.order'].create({
                                'partner_id': line.partner_id.id,
                                'date_order': demand.date_requisition,
                                'date_planned': demand.schedule_date,
                                'company_id': demand.company_id.id,
                                'purchase_demand_id': demand.id,
                                'notes': demand.description,
                                'state': 'draft',
                            })
                            pvals = {
                                'product_id': line.product_id.id,
                                'name': line.name,
                                'product_qty': line.product_uom_qty,
                                'product_uom':line.product_uom.id,
                                'price_unit':1,
                                'order_id': purchase_id.id,
                                'purchase_demand_line_id': line.id,
                            }
                            purchase_line_id = self.env['purchase.order.line'].create(pvals)
            
    
    @api.depends('purchase_ids')
    def _compute_orders_number(self):
        for demand in self:
            demand.order_count = len(demand.purchase_ids)

   
    
    
class PurchaseDemandLine(models.Model):
    _name = 'purchase.demand.line'
    _description = 'Purchase Demand Line'
    
    purchase_demand_id = fields.Many2one('purchase.demand', string='Purchase Demand', required=True, ondelete='cascade', index=True, copy=False)
    demand_action = fields.Selection([
        ('purchase', 'External'),
        ], string='Requisition Action', default='purchase', ondelete='no action', required=True)
    state = fields.Selection(related='purchase_demand_id.state', readonly=True)
    employee_id = fields.Many2one('hr.employee', related='purchase_demand_id.employee_id', readonly=True)
    user_id = fields.Many2one('res.users', related='purchase_demand_id.user_id', readonly=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('purchase_ok', '=', True)]", change_default=True, ondelete='restrict', required=True) 
    product_template_id = fields.Many2one('product.template', string='Product Template',
        related="product_id.product_tmpl_id", domain=[('purchase_ok', '=', True)])
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', change_default=True, index=True, tracking=1)
    ordered_qty = fields.Float(string='Oredered Quantity', compute='get_qty')
    schedule_date = fields.Date(string='Scheduled Date')
    
    def get_qty(self):
        qty = 0
        for record in self:
            qty = 0
            purchases = self.env['purchase.order'].search([('purchase_demand_id', '=', record.purchase_demand_id.id),('partner_id','=',record.partner_id.id),('state','!=','cancel')])
            for purchase in purchases:
                qty += purchase.order_line.product_qty
            record.ordered_qty = qty
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
        if not self.schedule_date:
            self.schedule_date = self.purchase_demand_id.schedule_date