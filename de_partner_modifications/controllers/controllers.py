# -*- coding: utf-8 -*-
# from odoo import http


# class DePartnerModifications(http.Controller):
#     @http.route('/de_partner_modifications/de_partner_modifications/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_partner_modifications/de_partner_modifications/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_partner_modifications.listing', {
#             'root': '/de_partner_modifications/de_partner_modifications',
#             'objects': http.request.env['de_partner_modifications.de_partner_modifications'].search([]),
#         })

#     @http.route('/de_partner_modifications/de_partner_modifications/objects/<model("de_partner_modifications.de_partner_modifications"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_partner_modifications.object', {
#             'object': obj
#         })
