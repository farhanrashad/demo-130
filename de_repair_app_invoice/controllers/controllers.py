# -*- coding: utf-8 -*-
# from odoo import http


# class DeRepairAppInvoice(http.Controller):
#     @http.route('/de_repair_app_invoice/de_repair_app_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_repair_app_invoice/de_repair_app_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_repair_app_invoice.listing', {
#             'root': '/de_repair_app_invoice/de_repair_app_invoice',
#             'objects': http.request.env['de_repair_app_invoice.de_repair_app_invoice'].search([]),
#         })

#     @http.route('/de_repair_app_invoice/de_repair_app_invoice/objects/<model("de_repair_app_invoice.de_repair_app_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_repair_app_invoice.object', {
#             'object': obj
#         })
