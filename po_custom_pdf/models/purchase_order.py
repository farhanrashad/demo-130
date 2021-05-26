# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models,fields,api,_
import re
class PurchaseOrder(models.Model):
    _inherit='purchase.order'
    
    @api.model
    def get_reports_data(self):
        name=''
        final_dic={}
        product_dic={}
        value_ids=[]
        attribute_dic={}
        final_dic={}
        count=0
        for rec in self:
            for rec_line in rec.order_line:
                for line in rec_line.product_id.product_template_attribute_value_ids:
                    print("\n\n\n\nattribute",line.attribute_id.name)
                    print("\n\n\n\nvalue",line.product_attribute_value_id.name)
#                     for value in rec_line.product_id.product_tmpl_id.attribute_line_ids.value_ids:
#                         if value.attribute_id.id == line.attribute_id.id:
#                             if final_dic.get(value.name):
#                                 dic_emp = final_dic.get(value.name, {})
#                                 dic_inner_emp = {
#                                     'qty': rec_line.product_qty,
#                                     }
#                                 dic_emp.update({value.name :dic_inner_emp })
#                                 final_dic.update({
#                                     value.name : dic_emp
#                                     })
#                             else:
#                                 dic_emp = {}
#                                 dic_inner_emp = {
#                                     'qty': rec_line.product_qty,
#                                     }
#                                 dic_emp.update({value.name :dic_inner_emp })                    
#                                 final_dic.update({
#                                     value.name : dic_emp
#                                     })
        print("\n\n\n\nattribute_list",final_dic)
        return name