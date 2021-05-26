from odoo.exceptions import Warning
from openerp import models, fields, api, _
import xlrd
import tempfile
import binascii
from xlwt import Workbook
import re


# class producttemplate(models.Model):
#     _inherit = 'product.template'

#     vendor_product_name = fields.Char(string="Vendor Product Name")
#     vendor_code = fields.Char(string="Vendor Code")


class wizard_import_script(models.TransientModel):
    _name = "wizard.import.script"

    file = fields.Binary('File')

    @api.multi
    def import_product(self):
        if not self.file:
            raise Warning(_('please upload .xlsx file.'))
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        template_obj = self.env['product.template']
        #silhouette_obj = self.env['product.silhouette']
        #brand_obj = self.env['product.brand']
        #collection_obj = self.env['product.collection']
        #family_obj = self.env['product.family']
        categ_obj = self.env['product.category']
        #pos_categ_obj = self.env['pos.category']
        tax_obj = self.env['account.tax']
        attobj = self.env['product.attribute']
        avalobj = self.env['product.attribute.value']
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(map(lambda row:row.value, sheet.row(row_no)))
                if line and line[1]:
                    template_id = template_obj.search([('name', '=', line[2])])
                    if template_id:
                        print(line[2])
                        print("================Paki I RUn")
                        sVal = False
                        valss = {}
                        variant_Vals = []
                       
                        if line[4]:  # color
                            att_id = self.attribute_create(name='Color')
                            attribute_val_list = []
                            for each in line[4].split(','):
                                print(each)
                                a_v_id = self.attribute_value_create(att_id, each).id
                            variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(4,a_v_id)]}))
                        
                        
                        #style_product = self.env['product.template'].search([('name', '=', line[2]),('attribute_ids', 'in', att_id.id)], limit=1)
                        exist_attr = template_id.attribute_line_ids.search([('attribute_id', '=', att_id.id)])
                        print("YYYYY")
                        print(exist_attr)
                        
                        
                        valss.update({'attribute_line_ids': variant_Vals})
                        print("======================")
                        print(valss)
                        print("================AAAAAAAAA")
                        res = template_id.write(valss)
                        
                        
                        
                        
                        
                        
                        print(res)
                        
                       
                        
                        # if style_product:
                        #     for record in style_product:
                        #         record.write({
                        #             'barcode': line[1] or ''
                        #             })

                        continue
                    
                        
                    
                    
                    vals = {'name': line[2],
                            #'vendor_product_name': line[3] or '',
                            'standard_price': line[6] or 0,
                            'list_price': line[7] or 0,
                            #'description_sale':line[17],
                            }
                    # if line[2]:
                    #     product_type = line[2].title()
                    #     final_type = False
                    #     if product_type == 'Stockable Product':
                    #         final_type = 'product'
                    #     if product_type == 'Consumable':
                    #         final_type = 'consu'
                    #     if product_type == 'Service':
                    #         final_type = 'service'
                    #     if final_type:
                    #         vals.update({'type':final_type})

                    print("================Paki")
                    print(line[2])
                    sVal = False
                    variant_Vals = []
                    if line[5]:  # Size
                        att_id = self.attribute_create(name='Size')
                        attribute_val_list = []
                        sVal = int(line[5])
                        for each in str(sVal).split(','):
                            attribute_val_list.append(self.attribute_value_create(att_id, each).id)
                        variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
                    if line[4]:  # color
                        att_id = self.attribute_create(name='Color')
                        attribute_val_list = []
                        for each in line[4].split(','):
                            attribute_val_list.append(self.attribute_value_create(att_id, each).id)
                        variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
                    
                    if line[3]:  # style
                        att_id = self.attribute_create(name='Style')
                        attribute_val_list = []
                        for each in line[3].split(','):
                            attribute_val_list.append(self.attribute_value_create(att_id, each).id)
                        variant_Vals.append((0, 0, {'attribute_id': att_id.id, 'value_ids': [(6, 0, attribute_val_list)]}))
                    
                    vals.update({'attribute_line_ids': variant_Vals,
                                 #'vendor_code': line[13] or '',
                                 'default_code': line[0] or '',
                                 #'barcode': line[1] or ''
                                 })
                    # if line[14]:
                    #     categ_id = categ_obj.search([('name', '=', line[14])], limit=1)
                    #     if not categ_id:
                    #         categ_id = categ_obj.create({'name': line[14]})
                    #     vals.update({'categ_id': categ_id.id})

                    # # Product Brand
                    # if line[10]:
                    #     brand_id = brand_obj.search([('name', '=', line[10])], limit=1)
                    #     if not brand_id:
                    #         brand_id = brand_obj.create({'name': line[10]})
                    #     vals.update({'product_brand_id': brand_id.id})

                    # # Product Collection
                    # if line[11]:
                    #     collection_id = collection_obj.search([('name', '=', line[11])], limit=1)
                    #     if not collection_id:
                    #         collection_id = collection_obj.create({'name': line[11]})
                    #     vals.update({'product_collection_id': collection_id.id})

                    # # Product Family
                    # if line[12]:
                    #     family_id = family_obj.search([('name', '=', line[12])], limit=1)
                    #     if not family_id:
                    #         family_id = family_obj.create({'name': line[12]})
                    #     vals.update({'product_family_id': family_id.id})

                    # # Product Silhouette
                    # if line[13]:
                    #     silhouette_id = silhouette_obj.search([('name', '=', line[13])], limit=1)
                    #     if not silhouette_id:
                    #         silhouette_id = silhouette_obj.create({'name': line[13]})
                    #     vals.update({'product_silhouette_id': silhouette_id.id})
                    
                    res = template_obj.create(vals)
        return True

    @api.multi
    def attribute_create(self, name):
        attobj = self.env['product.attribute']
        att_id = attobj.search([('name', '=', name)], limit=1)
        if not att_id:
            att_id = attobj.create({'name': name})
        return att_id

    @api.multi
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
            dups = self.env['mail.followers'].search([('res_model', '=',vals.get('res_model')),
                                                ('res_id', '=', vals.get('res_id')),
                                                ('partner_id', '=', vals.get('partner_id'))])
            if len(dups):
                for p in dups:
                    p.unlink()
        res = super(Followers, self).create(vals)
        return res