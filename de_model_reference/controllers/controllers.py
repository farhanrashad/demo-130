# -*- coding: utf-8 -*-
from odoo import http

# class DeModalReference(http.Controller):
#     @http.route('/de_modal_reference/de_modal_reference/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_modal_reference/de_modal_reference/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_modal_reference.listing', {
#             'root': '/de_modal_reference/de_modal_reference',
#             'objects': http.request.env['de_modal_reference.de_modal_reference'].search([]),
#         })

#     @http.route('/de_modal_reference/de_modal_reference/objects/<model("de_modal_reference.de_modal_reference"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_modal_reference.object', {
#             'object': obj
#         })