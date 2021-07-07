# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015 Dynexcel (<http://dynexcel.com/>).
#
##############################################################################

import time

from odoo import fields,api,models
from dateutil import parser
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class MaterialRequirementWizard(models.TransientModel):
    _name = 'material.requirement.wizard'
    _description = 'Material Requirement Wizard'


    activity_id = fields.Many2many('stock.picking')


    def print_report(self):

        data = {}
        data['form'] = self.read(['activity_id'])[0]
        return self.env.ref('de_material_requirement_report.material_requirement_report_record').report_action(self,data=data,
                                                                                                      config=False)


class MaterialRequirementData(models.Model):
    _name = 'material.requirement.data'
    _rec_name = 'product_id'



    activity_id = fields.Integer(string='Activity')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    mr_demand = fields.Float(string='Demand')
    mr_uom = fields.Many2one('uom.uom', string='UOM')
    mr_reserved = fields.Float(string='Reserved')
