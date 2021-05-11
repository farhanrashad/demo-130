# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class ProductTemplate(models.Model):
    _inherit='product.template'
    
    product_property_line=fields.One2many('product.properties.lines','property_ids',string="Product Property Lines")
    internal_code = fields.Char('Fabric Code')
    pct_code = fields.Char(string='PCT Code')
    
    fabric_product_id = fields.Many2one('product.product', string="Fabric", domain="[('categ_id.category_type', '=', 'fabric')]")
    style_product_id = fields.Many2one('product.product', string="Style", domain="[('categ_id.category_type', '=', 'style')]") 

    
    @api.model
    def _prepare_product_vals(self, values):
        return {'name': values['name']}
    
#     def write(self, vals):
#         self.ensure_one()
#         pname = pcode = ''
#         for property in self.product_property_line.sorted(key=lambda r: r.long_sequence):
#             if property.is_long:
#                 pname += property.description + ' '
#         for property in self.product_property_line.sorted(key=lambda r: r.short_sequence):
#             if property.is_short:
#                 pcode += property.product_property_line_id.name + '|'
#         if not pname:
#             pname = 'New'
        
#         vals['name'] = pname[:-1]
#         vals['default_code'] = pcode[:-1]
#         #self.default_code = pcode
#         result = super(ProductTemplate, self).write(vals)
#         return result

    def copy(self):
        res = super(ProductTemplate, self).copy()
        data = []
        for property in self.product_property_line:
            data.append((0,0,{
                'product_property_id' : property.product_property_id.id,
                'product_property_line_id' : property.product_property_line_id.id,
                'description' : property.description,
                'property_factory_ref_no' : property.property_factory_ref_no,
                'is_long' : property.is_long,
                'is_short' : property.is_short,
                'is_property_factory_ref_no' : property.is_property_factory_ref_no,
            }))
        res.product_property_line = data
        res._onchange_property_line()
        return res




    @api.onchange('product_property_line', 'default_code')
    def _onchange_property_line(self):
        pname = pcode = ''
        for property in self.product_property_line.sorted(key=lambda r: r.sequence):
            if property.is_long:
                if property.description:
                    pname += property.description + ' '
        for property in self.product_property_line.sorted(key=lambda r: r.short_sequence):
            if property.is_short:
                if property.product_property_line_id.name:
                    pcode += property.product_property_line_id.name + '|'
        if not pname:
            pname = 'New '
        self.update({
            'name': pname[:-1],
            'default_code': pcode[:-1],
        })
        
    @api.onchange('fabric_product_id')
    def onchange_fabric_product(self):
        if self.product_property_line:
            self.product_property_line.unlink()
        fdata = []
        if self.fabric_product_id:
            for property in self.fabric_product_id.product_property_line:
                fdata.append((0,0,{
                    'product_property_id': property.product_property_id.id,
                    'description': property.description,
                    'product_property_line_id': property.product_property_line_id.id,
                }))
            self.product_property_line = fdata
        
    @api.onchange('style_product_id')
    def onchange_style_product(self):
        #if self.fabric_product_id:
         #   if self.product_property_line:
          #      self.product_property_line.unlink()
        sdata = []
        if self.style_product_id:
            for property in self.style_product_id.product_property_line:
                sdata.append((0,0,{
                    'product_property_id': property.product_property_id.id,
                    'description': property.description,
                    'product_property_line_id': property.product_property_line_id.id,
                }))
        self.product_property_line = sdata
        #result = super(ProductTemplate, self).write(vals)
        #self.update({
        #    'product_property_line' : data
        #})
        
        #for product in product_ids:
        #    for property in product.product_property_line:
        #        data.append((0,0,{
        #                    'product_property_id': property.product_property_id.id,
        #                    'description': property.description,
        #                    'product_property_line_id': property.product_property_line_id.id,
        #                    }))
        
        

class ProductProductInh(models.Model):
    _inherit = 'product.product'


    factory_ref = fields.Char(compute="_compute_factory_ref", string='factory Ref')

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProductInh, self.with_context(create_product_product=True)).create(vals_list)
        self.clear_caches()
        for product in products:
            product._onchange_property_line()
        return products
    def _onchange_property_line(self):
        pname = pcode = pcode_1 = ''
        for property in self.product_property_line.sorted(key=lambda r: r.sequence):
            if property.is_long:
                if property.description:
                    pname += property.description + ' '
        for property in self.product_property_line.sorted(key=lambda r: r.short_sequence):
            if property.is_short:
                if property.product_property_line_id.name:
                    pcode_1 += property.product_property_line_id.name + '|'
                    pcode = pcode_1 + str(self.product_template_attribute_value_ids.name) + '|'
        if not pname:
            pname = 'New '
        self.update({
            'name': pname[:-1],
            'default_code': pcode[:-1],
        })
        
    @api.onchange('product_property_line', 'default_code')
    def _onchange_property_line(self):
        pname = pcode = pcode_1 = ''
        for property in self.product_property_line.sorted(key=lambda r: r.sequence):
            if property.is_long:
                if property.description:
                    pname += property.description + ' '
        for property in self.product_property_line.sorted(key=lambda r: r.short_sequence):
            if property.is_short:
                if property.product_property_line_id.name:
                    pcode_1 += property.product_property_line_id.name + '|'
                    pcode = pcode_1 + str(self.product_template_attribute_value_ids.name) + '|'
        if not pname:
            pname = 'New '
        self.update({
            'name': pname[:-1],
            'default_code': pcode[:-1],
        })
  
    @api.depends('product_tmpl_id.product_property_line','product_tmpl_id.product_property_line.property_factory_ref_no')
    def _compute_factory_ref(self):
        found = False
        property_sno = categ_sno = ''
        
        for rec in self:
            for property in rec.product_tmpl_id.product_property_line:
                if property.is_property_factory_ref_no == True:
                    property_sno = property.property_factory_ref_no
                    found = True
            
            if rec.categ_id:
                categ_sno = rec.categ_id.property_factory_ref_no
            if not property_sno:
                property_sno = ''
            if not categ_sno:
                property_sno =''
        self.factory_ref =  str(categ_sno)+ " | " +str(property_sno)


class product_template_line(models.Model):
    _name='product.properties.lines'
    _order = 'sequence'

    
    property_ids=fields.Many2one('product.template',string="Product Property Line", required=True)
    categ_id = fields.Many2one('product.category', related='property_ids.categ_id',string="Category")

    product_property_id=fields.Many2one("product.properties",string="Product Property", required=True, domain="[('categ_id','=',parent.categ_id)]")
    sequence = fields.Integer('Sequence', help="Determine the display order", index=True)
    product_property_line_id=fields.Many2one("product.properties.line",  string="Short Value", domain="[('product_property', '=', product_property_id)]")
    description = fields.Char(related='product_property_line_id.description', string='Long Value', store=True)
    property_factory_ref_no = fields.Char(related='product_property_line_id.property_factory_ref_no',)
    is_property_factory_ref_no = fields.Boolean(string='Is Pattern?', default=False)

    
    long_sequence = fields.Integer(related='product_property_id.long_sequence', readonly=True,)
    short_sequence = fields.Integer(related='product_property_id.short_sequence', readonly=True,)
    is_short = fields.Boolean(related="product_property_id.is_short", readonly=False, )
    is_long = fields.Boolean(related="product_property_id.is_long", readonly=False, )