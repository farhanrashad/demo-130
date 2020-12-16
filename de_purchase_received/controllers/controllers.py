# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseReceived(http.Controller):
#     @http.route('/de_purchase_received/de_purchase_received/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_received/de_purchase_received/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_received.listing', {
#             'root': '/de_purchase_received/de_purchase_received',
#             'objects': http.request.env['de_purchase_received.de_purchase_received'].search([]),
#         })

#     @http.route('/de_purchase_received/de_purchase_received/objects/<model("de_purchase_received.de_purchase_received"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_received.object', {
#             'object': obj
#         })
