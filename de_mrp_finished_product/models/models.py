# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_mrp_finished_product(models.Model):
#     _name = 'de_mrp_finished_product.de_mrp_finished_product'
#     _description = 'de_mrp_finished_product.de_mrp_finished_product'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
