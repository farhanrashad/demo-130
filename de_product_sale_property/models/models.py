# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class Productproperty(models.Model):
    _name='product.property'

    name=fields.Char(string="Product Property")
    is_long_value=fields.Boolean('Is Long Value')
    is_short_value=fields.Boolean('Is Short Value')
    long_value=fields.Many2many('product.long',string="Long Value")
    short_value=fields.Many2many('product.short',string="Short Value")
    
class Productlong(models.Model):
    _name='product.long'   
    name=fields.Char('Long Value')
    
class Productshort(models.Model):
    _name='product.short'
    
    name=fields.Char('Short Value') 
    
    
class product_product(models.Model):
    _inherit='product.template'
    
    product_property_order_line=fields.One2many("product.property.line","property_order")
    

    
class product_property_line(models.Model):
    _name='product.property.line'
    
    property_order=fields.Many2one("product.template",string="Product Property Order")   
    is_long_value=fields.Boolean('Is Long Value')
    is_short_value=fields.Boolean('Is Short Value')
    long_value=fields.Many2one('product.long',string="Long Value")
    short_value=fields.Many2one('product.short',string="Short Value")
    product_property=fields.Many2one('product.property',string="Product Property")
    
       
    @api.onchange('product_property','short_value')
    def onchange_short_ids(self):
        listids=[]
        domain={}
        if self.product_property.short_value:
            for ss in self.product_property.short_value:
                    listids.append(ss.id)

            return {'domain':{'short_value':[('id','in',listids)]}}
        
        
    @api.onchange('product_property','long_value')
    def onchange_long_ids(self):
        list_ids=[]
        domain={}
        if self.product_property.long_value:
            for ss in self.product_property.long_value:
                    list_ids.append(ss.id)

            return {'domain':{'long_value':[('id','in',list_ids)]}}
        
    def create(self, vals_list):
        if vals_list:
            list_1=[]
            list_2=[]
            j=0
            jj=0
            str1=" "
            for ss in vals_list:
                if ss.get('is_short_value')==True:
                    zz=self.env['product.short'].search([('id','=',ss.get('short_value'))])
                    list_1.append(zz.name+'&')

                if ss.get('is_long_value')==True:
                    zzz=self.env['product.long'].search([('id','=',ss.get('long_value'))])
                    list_2.append(zzz.name+' ')
            j=self.env['product.template'].search([('id','=',vals_list[0]['property_order'])])

            j.default_code=str(j.default_code)+(str1.join(list_1))           
            j.write({'name':j.name+(str1.join(list_2))})
        return super(product_property_line, self).create(vals_list)   
    
    def write(self, vals):
        if vals:
            if vals.get('is_short_value')==True:
                self.property_order.default_code=str(self.property_order.default_code)+self.short_value.name+'&'           
            if vals.get('is_long_value')==True:
                self.property_order.name=self.property_order.name+' '+self.long_value.name+' '
        return super(product_property_line, self).write(vals)   

    