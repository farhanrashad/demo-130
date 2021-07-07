# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountAssetNumber(http.Controller):
#     @http.route('/de_account_asset_number/de_account_asset_number/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_asset_number/de_account_asset_number/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_asset_number.listing', {
#             'root': '/de_account_asset_number/de_account_asset_number',
#             'objects': http.request.env['de_account_asset_number.de_account_asset_number'].search([]),
#         })

#     @http.route('/de_account_asset_number/de_account_asset_number/objects/<model("de_account_asset_number.de_account_asset_number"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_asset_number.object', {
#             'object': obj
#         })
