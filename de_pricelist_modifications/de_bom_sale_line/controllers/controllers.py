# -*- coding: utf-8 -*-
# from odoo import http


# class DeBomSaleLine(http.Controller):
#     @http.route('/de_bom_sale_line/de_bom_sale_line/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_bom_sale_line/de_bom_sale_line/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_bom_sale_line.listing', {
#             'root': '/de_bom_sale_line/de_bom_sale_line',
#             'objects': http.request.env['de_bom_sale_line.de_bom_sale_line'].search([]),
#         })

#     @http.route('/de_bom_sale_line/de_bom_sale_line/objects/<model("de_bom_sale_line.de_bom_sale_line"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_bom_sale_line.object', {
#             'object': obj
#         })
