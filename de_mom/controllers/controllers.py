# -*- coding: utf-8 -*-
# from odoo import http


# class DeMom(http.Controller):
#     @http.route('/de_mom/de_mom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_mom/de_mom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_mom.listing', {
#             'root': '/de_mom/de_mom',
#             'objects': http.request.env['de_mom.de_mom'].search([]),
#         })

#     @http.route('/de_mom/de_mom/objects/<model("de_mom.de_mom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_mom.object', {
#             'object': obj
#         })
