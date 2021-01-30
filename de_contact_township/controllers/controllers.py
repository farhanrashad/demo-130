# -*- coding: utf-8 -*-
# from odoo import http


# class DeContactTownship(http.Controller):
#     @http.route('/de_contact_township/de_contact_township/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_contact_township/de_contact_township/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_contact_township.listing', {
#             'root': '/de_contact_township/de_contact_township',
#             'objects': http.request.env['de_contact_township.de_contact_township'].search([]),
#         })

#     @http.route('/de_contact_township/de_contact_township/objects/<model("de_contact_township.de_contact_township"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_contact_township.object', {
#             'object': obj
#         })
