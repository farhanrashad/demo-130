# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductWarrenty(http.Controller):
#     @http.route('/de_product_warrenty/de_product_warrenty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_warrenty/de_product_warrenty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_warrenty.listing', {
#             'root': '/de_product_warrenty/de_product_warrenty',
#             'objects': http.request.env['de_product_warrenty.de_product_warrenty'].search([]),
#         })

#     @http.route('/de_product_warrenty/de_product_warrenty/objects/<model("de_product_warrenty.de_product_warrenty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_warrenty.object', {
#             'object': obj
#         })
