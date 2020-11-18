# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountAssetsDetails(http.Controller):
#     @http.route('/de_account_assets_details/de_account_assets_details/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_assets_details/de_account_assets_details/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_assets_details.listing', {
#             'root': '/de_account_assets_details/de_account_assets_details',
#             'objects': http.request.env['de_account_assets_details.de_account_assets_details'].search([]),
#         })

#     @http.route('/de_account_assets_details/de_account_assets_details/objects/<model("de_account_assets_details.de_account_assets_details"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_assets_details.object', {
#             'object': obj
#         })
