# -*- coding: utf-8 -*-
# from odoo import http


# class DeAccountMaintenanceOrder(http.Controller):
#     @http.route('/de_account_maintenance_order/de_account_maintenance_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_account_maintenance_order/de_account_maintenance_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_account_maintenance_order.listing', {
#             'root': '/de_account_maintenance_order/de_account_maintenance_order',
#             'objects': http.request.env['de_account_maintenance_order.de_account_maintenance_order'].search([]),
#         })

#     @http.route('/de_account_maintenance_order/de_account_maintenance_order/objects/<model("de_account_maintenance_order.de_account_maintenance_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_account_maintenance_order.object', {
#             'object': obj
#         })
