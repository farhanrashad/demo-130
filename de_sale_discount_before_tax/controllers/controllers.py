# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleDiscountBeforeTax(http.Controller):
#     @http.route('/de_sale_discount_before_tax/de_sale_discount_before_tax/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_discount_before_tax/de_sale_discount_before_tax/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_discount_before_tax.listing', {
#             'root': '/de_sale_discount_before_tax/de_sale_discount_before_tax',
#             'objects': http.request.env['de_sale_discount_before_tax.de_sale_discount_before_tax'].search([]),
#         })

#     @http.route('/de_sale_discount_before_tax/de_sale_discount_before_tax/objects/<model("de_sale_discount_before_tax.de_sale_discount_before_tax"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_discount_before_tax.object', {
#             'object': obj
#         })
