# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockTransferSec(http.Controller):
#     @http.route('/de_stock_transfer_sec/de_stock_transfer_sec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_transfer_sec/de_stock_transfer_sec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_transfer_sec.listing', {
#             'root': '/de_stock_transfer_sec/de_stock_transfer_sec',
#             'objects': http.request.env['de_stock_transfer_sec.de_stock_transfer_sec'].search([]),
#         })

#     @http.route('/de_stock_transfer_sec/de_stock_transfer_sec/objects/<model("de_stock_transfer_sec.de_stock_transfer_sec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_transfer_sec.object', {
#             'object': obj
#         })
