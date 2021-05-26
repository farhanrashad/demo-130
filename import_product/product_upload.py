from odoo.exceptions import Warning
from odoo import models, fields, api, _
import xlrd
import tempfile
import binascii
from xlwt import Workbook
import re
import datetime
import csv
import base64
import io as StringIO
from odoo.tools import ustr
# class producttemplate(models.Model):
#     _inherit = 'product.template'

#     vendor_product_name = fields.Char(string="Vendor Product Name")
#     vendor_code = fields.Char(string="Vendor Code")


class wizard_import_script(models.TransientModel):
    _name = "wizard.import.script"
    _description = "Import Wizard Script"
    file = fields.Binary('File')
    
    def import_product(self):
        line_ids = []
        attr_line_obj = self.env['product.template.attribute.line']
        product_obj = self.env['product.product']
        country_obj = self.env['res.country']
        hs_code_obj = self.env['hs.code']
        quality_obj = self.env['product.quality']
        fabric_obj = self.env['attribute.fabric']
        season_obj = self.env['attribute.season']
        year_obj = self.env['attribute.year']
        categ_obj = self.env['product.category']
        template_obj = self.env['product.template']
        
        can_be_purchase = False
        can_be_sold = False
        available_in_pos = False
        if not self.file:
            raise Warning(_('please upload CSV file.'))
        else:
            counter = 1
            file = str(base64.decodestring(self.file).decode('utf-8'))
            myreader = csv.reader(file.splitlines())
            skip_header = True
            counter_row = 1
            for row in myreader:
                tVal = False
                style = {}
                style_Vals = []
                size = {}
                brand_Vals = {}
                size_Vals = []
                color = {}
                color_Vals = []
                line_ids = []
                if skip_header:
                    skip_header = False
                    counter = counter + 1
                    counter_row += 1
                    continue
                template_id = self.env['product.template'].sudo().search([('sku', '=', row[0])])
                if template_id:
                    season_id = None
                    year_id = None
                    fit_id = None
                    fabric_consumption_id = None
                    collection_id = None
                    style_id = None
                    quality_id = None
                    fabric_id = None
                    if row[5]:
                        quality_id = quality_obj.sudo().search([('name', '=', row[5])], limit=1)
                    if row[6]:
                        fabric_id = fabric_obj.sudo().search([('name', '=', row[6])], limit=1)
                    if row[7]:
                        date = row[7]
                        converted_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
                        str_date = converted_date.strftime("%Y-%m-%d")
                        template_id.sudo().write({'launch_date':str_date})
                    if row[8]:
                        season_id = season_obj.sudo().search([('name', '=', row[8])], limit=1)
                    if row[9]:
                        year_id = year_obj.sudo().search([('name', '=', row[9])], limit=1)
                      
                    if row[10]:
                        fit_id = self.env['attribute.fit'].sudo().search([('name', '=', row[10])], limit=1)
                    if row[11]:
                        fabric_consumption_id = self.env['fabric.consumption'].sudo().search([('name', '=', row[11])], limit=1)
                    if row[12]:
                        collection_id = self.env['attribute.collection'].sudo().search([('name', '=', row[12])], limit=1)
                    if row[13]:
                        style_id = self.env['attribute.style'].sudo().search([('name', '=', row[13])], limit=1)
                    if row[14]:
                        template_id.sudo().write({'standard_price':row[14]})
                    if row[15]:
                        template_id.sudo().write({'list_price':row[15]})
                    if row[16]:
                        hs_code_id = hs_code_obj.sudo().search([('hs_code', '=', row[16])], limit=1)
                        if hs_code_id:
                            template_id.sudo().write({'hs_code_id':hs_code_id.id, })
                    if row[17]: 
                        country_id = country_obj.sudo().search([('name', 'ilike', row[17])], limit=1)
                        if country_id: 
                            template_id.sudo().write({'origin_country_id':country_id.id, })
                    if row[18] and row[18] == 'Storable Product':
                        final_type = 'product'
                    if row[18] and row[18] == 'Consumable Product':
                        final_type = 'consu'
                    if row[18] and row[18] == 'Service Product':
                        final_type = 'service'
                    if row[19] and row[19] == 'TRUE':
                        can_be_sold = True
                    if row[20] and row[20] == 'TRUE' :
                        can_be_purchase = True
                    if row[21]:
                        categ_id = categ_obj.sudo().search([('name', '=', row[21])], limit=1)
                        if categ_id:
                            template_id.sudo().write({'categ_id':categ_id.id, })
                    if row[24]:
                        unit_id = self.env['uom.uom'].sudo().search([('name','=',row[24])],limit=1)
                        if unit_id and template_id:
                            template_id.sudo().write({
                                'uom_id':unit_id.id,
                                })
                    if row[25]:
                        unit_id = self.env['uom.uom'].sudo().search([('name','=',row[25])],limit=1)
                        if unit_id and template_id:
                            template_id.sudo().write({
                                'uom_po_id':unit_id.id,
                                })
                    if row[26] and row[26] == 'TRUE' :
                        available_in_pos = True
                    if template_id:
                        template_id.sudo().write({'name':row[2], 'sale_ok':can_be_sold, 'purchase_ok':can_be_purchase, 'type':final_type,'available_in_pos':available_in_pos})
                    if template_id and fabric_id:
                        template_id.sudo().write({
                            'product_fabric_id':fabric_id.id,
                            })
                    if template_id and quality_id:
                        template_id.sudo().write({
                            'product_quality_id':quality_id.id,
                            })
                    if template_id and season_id:
                        template_id.sudo().write({
                            'product_season_id':season_id.id,
                            })
                    if template_id and year_id:
                        template_id.sudo().write({
                            'product_year_id':year_id.id,
                            })
                    if template_id and fit_id:
                        template_id.sudo().write({
                            'product_fit_id':fit_id.id,
                            })
                    if template_id and fabric_consumption_id:
                        template_id.sudo().write({
                            'fabric_consumption_id':fabric_consumption_id.id,
                            })
                    if template_id and collection_id:
                        template_id.sudo().write({
                            'collection_id':collection_id.id,
                            })
                    if template_id and style_id:
                        template_id.sudo().write({
                            'style_id':style_id.id,
                            })
#                     if row[3]:  # color
#                         if template_id.attribute_line_ids:
#                             for line in template_id.attribute_line_ids:
#                                 if line.attribute_id.name=='Color':
#                                     color = self.env['product.attribute'].sudo().search([('name','=','Color')],limit=1)
#                                     value = self.env['product.attribute.value'].sudo().search([('attribute_id','in',line.attribute_id.ids),('name','=',row[3])],limit=1)
#                                      
#                                     if color and value and not line.value_ids.name == row[3]:
#                                         color = [row[3]]
#                                         line.sudo().write({
#                                             'attribute_id':line.attribute_id.id,
#                                             'value_ids':[(6,0,color)]
#                                             })
#                                     else:
#                                         color_list = [row[3]]
#                                         color_id = self.env['product.attribute'].sudo().create({
#                                             'name':'Color',
#                                             })
#                                         value = self.env['product.attribute.value'].sudo().create({
#                                             'name':row[3],
#                                             'attribute_id':color_id.id,
#                                             })
#                                         line.sudo().write({
#                                             'attribute_id':color_id.id,
#                                             'value_ids':[(6,0,color_list)]
#                                             })
#                                      
#                         else:
#                             attribute_line=[]
#                             attribute = self.env['product.attribute'].sudo().search([('name','=','Color')],limit=1)
#                             value =[row[3]]
#                             if attribute:
#                                 vals={
#                                     'attribute_id':attribute.id,
#                                     'value_ids':[(6,0,value)],
#                                     }
#                                 attribute_line.append((0,0,vals))
#                             template_id.attribute_line_ids = attribute_line
#                             for attribute_line in template_id.attribute_line_ids:
#                                 if attribute_line.attribute_id.name=='Color':
#                                     if attribute_line.value_ids:
#                                         for value in attribute_line.value_ids:
#                                             print("\n\n\nvalue.name",value.name)
#                                             if not value.name==row[3]:
#                                                 value_id = self.env['product.attribute.value'].sudo().search([('name','=',row[3])],limit=1)
#                                                 color_Vals.append(value_id.id)
#                                                 attribute_line.sudo().write({'product_tmpl_id':template_id.id,'attribute_id':attribute_line.attribute_id.id,'value_ids':[(6,0,color_Vals)]})
#                     if row[4]:  # size
#                         if template_id.attribute_line_ids:
#                             for attribute_line in template_id.attribute_line_ids:
#                                 if attribute_line.attribute_id.name=='Size':
#                                     if attribute_line.value_ids:
#                                         for value in attribute_line.value_ids:
#                                             if not value.name==row[4]:
#                                                 value_id = self.env['product.attribute.value'].sudo().search([('name','=',row[4])],limit=1)
#                                                 size_Vals.append(value_id.id)
#                                                 attribute_line.sudo().write({
#                                                     'product_tmpl_id':template_id.id,
#                                                     'attribute_id':attribute_line.attribute_id.id,
#                                                     'value_ids':[(6,0,size_Vals)]
#                                                     })
                    if row[3]:
                        att_id = self.attribute_create(name='Color')
                        colors = False
                        a_v_id=None
                        if "/" in row[3]:
                            for each in row[3].split('/'):
                                colors = each
                                a_v_id = self.attribute_value_create(att_id, each).id
                        else:
                            colors = row[3]
                            a_v_id = self.attribute_value_create(att_id, colors).id
                        exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
                        if exist_attr:
                            color_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
                        else:
                            color_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
                    color.update({'attribute_line_ids': color_Vals})
                         
                    template_id.sudo().write(color)
                    if row[4]:  # size
                        att_id = self.attribute_create(name='Size')
                        tVal = row[4]
                        a_v_id = self.attribute_value_create(att_id, tVal).id
           
                        exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
                        if exist_attr:
                            size_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
                        else:
                            size_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
                       
                    size.update({'attribute_line_ids': size_Vals})
                         
                    template_id.sudo().write(size) 
                if not template_id:
                    season_id = None
                    year_id = None
                    fit_id = None
                    fabric_consumption_id = None
                    collection_id = None
                    style_id = None
                    quality_id = None
                    fabric_id = None
                    vals = {}
                    if row[0] != '':
                        if row[0]:
                            vals.update({
                                'sku':row[0],
                                })
#                         if row[1]:
#                             vals.update({
#                                 'barcode':row[1],
#                                 })
                        if row[2]:
                            vals.update({
                                'name':row[2],
                                })
#                         if row[3]:  # color
#                             color_attibute = self.env['product.attribute'].sudo().search([('name','=','Color')],limit=1)
#                             value_attibute = self.env['product.attribute.value'].sudo().search([('name','=',row[3])],limit=1)
# #                             if color_attibute:
# #                                 color_list.append((0,0,{'attribute_id':color_attibute.id}))
#                             if value_attibute:
#                                 color_list.append((0,0,{'attribute_id':color_attibute.id,'value_ids':[(6,0,value_attibute.ids)]}))
#                             vals.update({'attribute_line_ids': color_list})
#                         if row[4]:  # size
#                             size_attibute = self.env['product.attribute'].sudo().search([('name','=','Size')],limit=1)
#                             value_attibute = self.env['product.attribute.value'].sudo().search([('name','=',row[4])],limit=1)
# #                             if size_attibute:
# #                                 size_list.append((0,0,{'attribute_id':size_attibute.id}))
#                             if value_attibute:
#                                 size_list.append((0,0,{'attribute_id':size_attibute.id,'value_ids':[(6,0,value_attibute.ids)]}))
#                             vals.update({'attribute_line_ids': size_list})
                        if row[3]:
                            colors = False
                            att_id = self.attribute_create(name='Color')
                            a_v_id=None
                            if "/" in row[3]:
                                for each in row[3].split('/'):
                                    colors = each
                                    a_v_id = self.attribute_value_create(att_id, each).id
                            else:
                                colors = row[3]
                                a_v_id = self.attribute_value_create(att_id, colors).id
                            exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
                            if exist_attr:
                                color_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
                            else:
                                color_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
                            vals.update({'attribute_line_ids': color_Vals})
                        if row[4]:
                            att_id = self.attribute_create(name='Size')
                            tVal = row[4]
                            a_v_id = self.attribute_value_create(att_id, tVal).id
                            exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
                            if exist_attr:
                                size_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
                            else:
                                size_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
                        
                            vals.update({'attribute_line_ids': size_Vals})
                            
                        if row[5]:
                            quality_id = quality_obj.sudo().search([('name', '=', row[5])], limit=1)
                            if quality_id:
                                vals.update({'product_quality_id':quality_id.id, })
                        if row[6]:
                            fabric_id = fabric_obj.sudo().search([('name', '=', row[6])], limit=1)
                            if fabric_id:
                                vals.update({'product_fabric_id':fabric_id.id, })
                        if row[7]: 
                            date = row[7]
                            converted_date = datetime.datetime.strptime(date, "%d-%m-%Y").date()
                            str_date = converted_date.strftime("%Y-%m-%d")
                            vals.update({'launch_date':str_date, })
                        if row[8]:
                            season_id = season_obj.sudo().search([('name', '=', row[8])], limit=1)
                            if season_id:
                                vals.update({'product_season_id':season_id.id})
                        if row[9]:
                            year_id = year_obj.sudo().search([('name', '=', row[9])], limit=1)
                            if year_id:
                                vals.update({'product_year_id':year_id.id, })
                        if row[10]:
                            search_fit = self.env['attribute.fit'].sudo().search([('name', '=', row[10])], limit=1)
                            if search_fit:
                                vals.update({'product_fit_id':search_fit.id})
                        if row[11]:
                            fabric_consumption = self.env['fabric.consumption'].sudo().search([('name', '=', row[11])], limit=1)
                            if fabric_consumption:
                                vals.update({
                                    'fabric_consumption_id':fabric_consumption.id,
                                    })
                        if row[12]:
                            collection_id = self.env['attribute.collection'].sudo().search([('name', '=', row[12])], limit=1)
                            if collection_id:
                                vals.update({
                                    'collection_id':collection_id.id,
                                    })
                        if row[13]:
                            style_id = self.env['attribute.style'].sudo().search([('name', '=', row[13])], limit=1)
                            if style_id:
                                vals.update({
                                    'style_id':style_id.id,
                                    })
                          
                        if row[14]:
                            vals.update({'standard_price':row[14]})
                        if row[15]:
                            vals.update({'list_price':row[15]})
                        if row[16]:
                            hs_code_id = hs_code_obj.sudo().search([('hs_code', '=', row[16])], limit=1)
                            if hs_code_id:
                                vals.update({'hs_code_id':hs_code_id.id, })
                        if row[17]: 
                            country_id = country_obj.sudo().search([('name', 'ilike', row[17])], limit=1)
                            if country_id: 
                                vals.update({'origin_country_id':country_id.id, })
                        if row[18] and row[18] == 'Storable Product':
                            final_type = 'product'
                            vals.update({'type':final_type})
                        if row[18] and row[18] == 'Consumable Product':
                            final_type = 'consu'
                            vals.update({'type':final_type})
                        if row[18] and row[18] == 'Service Product':
                            final_type = 'service'
                            vals.update({'type':final_type})
                        if row[19] and row[19] == 'TRUE':
                            can_be_sold = True
                            vals.update({'sale_ok':can_be_sold or False})
                        if row[20] and row[20] == 'TRUE' :
                            can_be_purchase = True
                            vals.update({'purchase_ok':can_be_purchase or False})
                        if row[21]:
                            categ_id = categ_obj.sudo().search([('name', '=', row[21])], limit=1)
                            if categ_id:
                                vals.update({'categ_id':categ_id.id, })
                        if row[24]:
                            unit_id = self.env['uom.uom'].sudo().search([('name','=',row[24])],limit=1)
                            if unit_id:
                                vals.update({
                                    'uom_id':unit_id.id,
                                    })
                        if row[25]:
                            unit_id = self.env['uom.uom'].sudo().search([('name','=',row[25])],limit=1)
                            if unit_id:
                                vals.update({
                                    'uom_po_id':unit_id.id,
                                    })
                        if row[26] and row[26] == 'TRUE' :
                            available_in_pos = True
                            vals.update({'available_in_pos':available_in_pos or False})
                        template_obj.sudo().create(vals)
                if row:
                    product_template_id = template_obj.search([('sku', '=', row[0])])
                    for template in product_template_id: 
                        if template:   
                            product_template_attribute_value_obj = self.env['product.template.attribute.value']
                            color = False
                            if "/" in row[3]:
                                for each in row[3].split('/'):
                                    color = each
                            else:
                                color = row[3]
                            str_size = row[4]
                            list_attribute_value_ids = []
                                
                            search_attribute_color = False
                            search_attribute_color = product_template_attribute_value_obj.sudo().search([
                                    ('attribute_id.name', '=', 'Color'),
                                    ('product_attribute_value_id.name', '=', color),
                                    ('product_tmpl_id', '=', template.id),
                                ])
                            if search_attribute_color:
                                for attribute in search_attribute_color:
                                    list_attribute_value_ids.append(attribute.id)
                                    
                            search_attribute_size = False
                            search_attribute_size = product_template_attribute_value_obj.sudo().search([
                                    ('attribute_id.name', '=', 'Size'),
                                    ('product_attribute_value_id.name', '=', str_size),
                                    ('product_tmpl_id', '=', template.id),
                                ])
                            if search_attribute_size:
                                for attribute in search_attribute_size:
                                    list_attribute_value_ids.append(attribute.id)
                            for product_varient in template.product_variant_ids:
                                if product_varient.product_template_attribute_value_ids.ids == list_attribute_value_ids:
#                                     if not product_varient.barcode and not product_varient.sku:
                                        product_varient.sudo().write({
                                            'barcode'      :row[1],
                                            'sku' :row[0],
                                            'weight':row[22],
                                            'volume':row[23],
                                            })
                product_id = self.env['product.product'].sudo().search([('sku','=',row[0])])
                for product in product_id:
                    product.sudo().write({
                        'default_code':product.sku,
                        })
                    product.product_tmpl_id.default_code = product.sku
                    # softhealer technologies code end on 20/11/2019
    # softhealer technologies code commented on 20/11/2019
#                 default_code_str = ''
#                 barcode_str = ''
#                 if line[14]:
#                     default_code_int = int(line[14])
#                     default_code_str = str(default_code_int)
#                 if line[15]:
#                     barcode_int = int(line[15])
#                     barcode_str = str(barcode_int)
#                 if line and line[2]:
#                     prod_name = str(line[2]).strip()
#                     template_id = template_obj.search([('name', '=', line[1])])
#                     
#                     if template_id:
#                        
#                         tVal = False
#                         style = {}
#                         style_Vals = []
#                         size = {}
#                         brand_Vals = {}
#                         size_Vals = []
#                         color = {}
#                         color_Vals = []
#                         if line[3]:  # style
#                             att_id = self.attribute_create(name='Style')
#                             for each in line[3].split(','):
#                                 a_v_id = self.attribute_value_create(att_id, each).id
# 
#                             exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
#                             if exist_attr:
#                                 style_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
#                             else:
#                                 style_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
#                         
#                         style.update({'attribute_line_ids': style_Vals})
# 
#                         res = template_id.write(style)
#                         
#                         if line[4]:  # color
#                             att_id = self.attribute_create(name='Color')
#                             for each in line[4].split(','):
#                                 a_v_id = self.attribute_value_create(att_id, each).id
# 
#                             exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
#                             if exist_attr:
#                                 color_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
#                             else:
#                                 color_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
#                         
#                         color.update({'attribute_line_ids': color_Vals})
# 
#                         res = template_id.write(color)
#                         
#                         if line[5]:  # size
#                             att_id = self.attribute_create(name='Size')
#                             tVal = line[5]
#                             for each in str(tVal).split(','):
#                                 a_v_id = self.attribute_value_create(att_id, each).id
# 
#                             exist_attr = attr_line_obj.search([('product_tmpl_id', '=', template_id.id), ('attribute_id', '=', att_id.id)], limit=1)
#                             if exist_attr:
#                                 size_Vals.append((1, exist_attr.id, {'value_ids': [(4, a_v_id)]}))
#                             else:
#                                 size_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4, a_v_id)]}))
#                     
#                         size.update({'attribute_line_ids': size_Vals})
# 
#                         res = template_id.write(size)
#                         
#                         product_obj = self.env['product.product'].search([('name', '=', prod_name),
#                                                ('attribute_value_ids.name', '=', line[3]),
#                                                ('attribute_value_ids.name', '=', line[4]),
#                                                ('attribute_value_ids.name', '=', str(line[5]))], limit=1)
#                         
#                         res = product_obj.write({
#                                 'default_code': line[0] or 0,
#                                 'barcode': line[1] or 0,
#                                             })
#                         continue
#                     else:
#                         # prod_name = str(line[2]).strip()
#                         vals = {'name': prod_name,
#                                 'default_code': line[0] or 0,
#                                 'barcode': line[1] or 0,
#                                 'standard_price': line[9] or 0,
#                                 'list_price': line[10] or 0,
#                                 'sale_ok': line[14] or 0,
#                                 'purchase_ok': line[15] or 0,
#                                 # 'description_sale':line[17],
#                                 }
#                         if line[13]:
#                             prod_type = line[13].title()
#                             prod_type = str(prod_type).strip()
#                             product_type = prod_type
#                             final_type = False
#                             if product_type == 'Storable':
#                                 final_type = 'product'
#                             if product_type == 'Consumable':
#                                 final_type = 'consu'
#                             if product_type == 'Service':
#                                 final_type = 'service'
#                             if final_type:
#                                 vals.update({'type':final_type})
#     
#                         sVal = False
#                         variant_Vals = []
#                         if line[5]:  # Size
#                             att_id = self.attribute_create(name='Size')
#                             attribute_val_list = []
#                             sVal = line[5]
#                             for each in str(sVal).split(','):
#                                 attribute_val_list.append(self.attribute_value_create(att_id, each).id)
#                             variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
#                         if line[4]:  # color
#                             att_id = self.attribute_create(name='Color')
#                             attribute_val_list = []
#                             for each in line[4].split(','):
#                                 attribute_val_list.append(self.attribute_value_create(att_id, each).id)
#                             variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
#                         
#                         if line[3]:  # style
#                             att_id = self.attribute_create(name='Style')
#                             attribute_val_list = []
#                             for each in line[3].split(','):
#                                 attribute_val_list.append(self.attribute_value_create(att_id, each).id)
#                             variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
#                         
#                         vals.update({'attribute_line_ids': variant_Vals,
#                                      })
#                        
#                         # Product Category
#                         if line[16]:
#                             categ_id = categ_obj.search([('complete_name', '=', line[16])], limit=1)
#                             if not categ_id:
#                                 categ_id = categ_obj.search([('name', '=', 'All')], limit=1)
#                             vals.update({'categ_id': categ_id.id})
#     
#                         # Product Collection
#                         if line[7]:
#                             collection_id = collection_obj.search([('name', '=', line[7])], limit=1)
#                             if not collection_id:
#                                 collection_id = collection_obj.create({'name': line[7]})
#                             vals.update({'product_collection_id': collection_id.id})
#     
#                         # Product Conversion
#                         if line[8]:
#                             conversion_id = conversion_obj.search([('name', '=', line[8])], limit=1)
#                             if not conversion_id:
#                                 conversion_id = conversion_obj.create({'name': line[8]})
#                             vals.update({'product_conversion_id': conversion_id.id})
#     
#                         # Product Silhouette
#                         if line[6]:
#                             silhouette_id = silhouette_obj.search([('name', '=', line[6])], limit=1)
#                             if not silhouette_id:
#                                 silhouette_id = silhouette_obj.create({'name': line[6]})
#                             vals.update({'product_silhouette_id': silhouette_id.id})
#                         
#                         # Country
#                         if line[12]:
#                             country_id = country_obj.search([('name', '=', line[12])], limit=1)
#                             if not country_id:
#                                 country_id = country_obj.create({'name': line[12]})
#                             vals.update({'origin_country_id': country_id.id})
#                         
#                         # Hs Code
#                         if line[11]:
#                             hs_code_id = hs_code_obj.search([('local_code', '=', line[11])], limit=1)
#                             if not hs_code_id:
#                                 hs_code_id = hs_code_obj.create({'local_code': line[11]})
#                             vals.update({'hs_code_id': hs_code_id.id})
#                         
#                         if not categ_id.name == 'All':
#                             res = template_obj.create(vals)
# 
#         # dele = self.env["product.product"].search([('barcode','=',False)]).unlink()            
#         return True

    def attribute_create(self, name):
        attobj = self.env['product.attribute']
        att_id = attobj.search([('name', '=', name)], limit=1)
        if not att_id:
            att_id = attobj.create({'name': name})
        return att_id

    def attribute_value_create(self, att_id, name):
        attobj = self.env['product.attribute.value']
        valueid = attobj.search([('name', '=', name), ('attribute_id', '=', att_id.id)], limit=1)
        if not valueid:
            valueid = attobj.create({'name': name, 'attribute_id': att_id.id})
        return valueid


class Followers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def create(self, vals):
        if 'res_model' in vals and 'res_id' in vals and 'partner_id' in vals:
            dups = self.env['mail.followers'].search([('res_model', '=', vals.get('res_model')),
                                                ('res_id', '=', vals.get('res_id')),
                                                ('partner_id', '=', vals.get('partner_id'))])
            if len(dups):
                for p in dups:
                    p.unlink()
        res = super(Followers, self).create(vals)
        return res
