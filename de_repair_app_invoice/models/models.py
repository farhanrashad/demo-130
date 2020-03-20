# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_repair_app_invoice(models.Model):
#     _name = 'de_repair_app_invoice.de_repair_app_invoice'
#     _description = 'de_repair_app_invoice.de_repair_app_invoice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
