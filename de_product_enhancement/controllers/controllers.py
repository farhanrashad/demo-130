# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductEnhancement(http.Controller):
#     @http.route('/de_product_enhancement/de_product_enhancement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_enhancement/de_product_enhancement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_enhancement.listing', {
#             'root': '/de_product_enhancement/de_product_enhancement',
#             'objects': http.request.env['de_product_enhancement.de_product_enhancement'].search([]),
#         })

#     @http.route('/de_product_enhancement/de_product_enhancement/objects/<model("de_product_enhancement.de_product_enhancement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_enhancement.object', {
#             'object': obj
#         })
