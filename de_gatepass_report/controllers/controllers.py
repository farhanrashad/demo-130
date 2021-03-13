# -*- coding: utf-8 -*-
# from odoo import http


# class DeGatepassReport(http.Controller):
#     @http.route('/de_gatepass_report/de_gatepass_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_gatepass_report/de_gatepass_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_gatepass_report.listing', {
#             'root': '/de_gatepass_report/de_gatepass_report',
#             'objects': http.request.env['de_gatepass_report.de_gatepass_report'].search([]),
#         })

#     @http.route('/de_gatepass_report/de_gatepass_report/objects/<model("de_gatepass_report.de_gatepass_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_gatepass_report.object', {
#             'object': obj
#         })
