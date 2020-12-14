# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class de_website_age_verification(models.Model):
#     _name = 'de_website_age_verification.de_website_age_verification'
#     _description = 'de_website_age_verification.de_website_age_verification'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
