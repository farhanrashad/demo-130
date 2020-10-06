# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class SaleReport(models.Model):
#     _inherit = "sale.report"
    
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['sale.order'].browse(docids)
#         production = self.env['mrp.production'].search([('origin','=', self.name)])
#         return {
#             'doc_ids': docs.ids,
#             'doc_model': 'sale.order',
#             'docs': docs,
# #             'production': production,  
#             'proforma': True
#         }
    
#     def production_order(self,txt):
#         production = self.env['mrp.production'].search([('origin','=', txt)])
#         return production
