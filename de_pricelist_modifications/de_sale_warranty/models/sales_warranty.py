# -*- coding: utf-8 -*-

import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime, timedelta



from odoo.addons import decimal_precision as dp


class SalesWarrenty(models.Model):
    _name = 'sales.warranty'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Sale Warranty'
    _order = 'id desc'
    
    name = fields.Char(string='Name',  copy=False,  index=True, default=lambda self: _('New'))
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Active', default=True)
    product_id = fields.Many2one('product.product',string='Product', track_visibility='onchange', required=True, readonly=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    #sno = fields.Char(string='Serial No',track_visibility='onchange', readonly=True,states={'draft': [('readonly', False)]},)
    lot_id = fields.Many2one('stock.production.lot',domain="[('product_id', '=', product_id)]",states={'draft': [('readonly', False)]},)
    partner_id = fields.Many2one('res.partner',string='Customer', required=True, track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    sale_id = fields.Many2one('sale.order', string='SO Reference', readonly=True)
    warranty_type = fields.Selection(string='Warranty Type', required=True, default='product', help="Type or Mode of the gatepass", selection=[('service', 'Service'), ('product', 'Product')])
    picking_id = fields.Many2one('stock.picking', string='Delivery Reference', readonly=True)
    invoice_id = fields.Many2one('account.invoice',string='Invoice Reference',readonly=True)
    purchase_date = fields.Date(string='Date of Purchase',required=True, readonly=True, states={'draft': [('readonly', False)]})
    warranty_start_date = fields.Date(string='Warranty Start Date',track_visibility='onchange',required=True, readonly=True, states={'draft': [('readonly', False)]})
    warranty_end_date = fields.Date(string='Warranty End Date',track_visibility='onchange',required=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft','Draft'),
                              ('inwarranty','In Warranty'),
                              ('toexpire','To Expire'),
                              ('expired','Expired')],string = "Status", default='draft',track_visibility='onchange')
    
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    quantity=fields.Float("Quantity")
    
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.warranty_start_date = datetime.date.today()
        if self.product_id.warranty_period == 'y':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=(self.product_id.warranty_period_interval*365))
        elif self.product_id.warranty_period == 'm':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=(self.product_id.warranty_period_interval*30))
        elif self.product_id.warranty_period == 'd':
            self.warranty_end_date = self.warranty_start_date + datetime.timedelta(days=self.product_id.warranty_period_interval)
    
    @api.model
    def create(self,values):
        seq = self.env['ir.sequence'].get('sales.warranty') 
        values['name'] = seq
        res = super(SalesWarrenty,self).create(values)
        return res    
        
    def start_warranty(self):
        warranty = self.env['sales.warranty'].search([
            ('partner_id','=',self.partner_id.id),
            ('product_id','=',self.product_id.id),
            ('lot_id','=', self.lot_id.id),
            ('state','=','inwarranty'),
        ])
        if len(warranty):
            raise UserError(_('Product is already in-warrany.'))
        else:
            self.state = 'inwarranty'
    
    def force_expire_warranty(self):
        self.state = 'expired'
        
    def unlink(self):
        for rs in self:
            if rs.state not in ('draft'):
                raise UserError(_('You can not delete a running warranty.'))
        return super(SalesWarrenty, self).unlink()
    
    @api.model
    def cron_warranty_expire(self):
        date_eval =  datetime.now()+timedelta(days=30)
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty = self.env['sales.warranty'].search([('warranty_end_date','<=',date_eval_str),
                                                                ('state','=','inwarranty')])
        for wty in warranty:                        
            wty.state = 'toexpire'
     
    @api.model
    def cron_warranty_expired(self):
        date_eval =  datetime.now()
        date_eval_str = date_eval.strftime('%Y-%m-%d')
        warranty = self.env['sales.warranty'].search([('warranty_end_date','<=',date_eval_str)])
        for wty in warranty:                        
            wty.state = 'expired'    
            
            
            
class wizard_stock(models.Model):
    _inherit = 'stock.move'
    
    def trigger_on_save(self):
        if self:
            for s in self:
                z=0
                if s.product_id.warranty_period_interval:
                    if s.product_id.warranty_period=='d':
                        z=s.product_id.warranty_period_interval
                    if s.product_id.warranty_period=='m':
                        z=s.product_id.warranty_period_interval*30
                    if s.product_id.warranty_period=='y':
                        z=s.product_id.warranty_period_interval*365
                        
                for ss in s.move_line_ids:
        
                    self.env['sales.warranty'].create({'partner_id': s.picking_id.partner_id.id,
                                            'warranty_start_date':s.picking_id.scheduled_date,
                                            'warranty_end_date':s.picking_id.scheduled_date+timedelta(z),
                                            'lot_id':ss.lot_id.id,
                                            'purchase_date':s.picking_id.scheduled_date,
                                            'quantity':ss.qty_done,
                                            'sale_id':s.picking_id.group_id.id,
                                            'product_id':s.product_id.id,
                                            'picking_id':s.picking_id.id,
                                            })


# class ConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
# 
#     warranty_policy = fields.Selection([
#         ('order', 'Ordered Warranty'),
#         ('delivery', 'Delivered Warranty')], string='Warranty Policy',
#         help='Ordered Warranty: Warranty starts on order confrimation.\n'
#              'Delivered Warranty: Warranty starts on delivered quantity.',
#         default='order', domain="[('type', '=', 'product')" )
#     
#     warranty_period = fields.Selection([
#         ('d', 'Day(s)'),
#         ('m', 'Month(s)'),
#         ('y', 'Year(s)')], string='Warranty Period',
#         help='Day(s): Warranty period 1-30 days.\n'
#              'Month(s): Warranty period in 1-12 months.\n'
#              'Month(s): Warranty period in year(s).',
#         default='d')
#     
#     warranty_period_interval = fields.Integer('Internval')

    
#     @api.multi
#     def set_values(self):
#         res = super(ConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].set_param('so_stock_details.check_product_stock', self.check_product_stock)
#         return res
# 
#     @api.model
#     def get_values(self):
#         res = super(ConfigSettings, self).get_values()
#         ICPSudo = self.env['ir.config_parameter'].sudo()
#         stock = ICPSudo.get_param('so_stock_details.check_product_stock')
#         res.update(
#             check_product_stock = stock,
#         )
#         return res
# 
class SalesSettings(models.Model):
    _inherit = 'product.template'
#      
#     def write(self, vals):
#         super(SalesSettings, self).write(vals) #--call parent class's method, you can also use, "super().write(vals)" in v13 no need to give class name and self
#             us=[]
#             confi = self.env['res.config.settings'].search([])
#             for i in confi:
#                 us.append(i)
#             jd=sorted(us)
#             aa=jd[-1]
#             print(aa)
    @api.model
    def create(self, vals):
        if 'is_warranty' not in vals or vals['is_warranty'] == 'True':
            conf = self.env['res.config.settings'].search([])
            vals['default_warranty_policy'] = conf.default_warranty_policy
            vals['default_warranty_period'] = conf.default_warranty_period
            vals['warranty_period_interval'] = conf.warranty_period_interval
        return super(SalesSettings, self).create(vals)
    
    
    