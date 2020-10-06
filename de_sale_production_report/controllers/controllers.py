# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleProductionReport(http.Controller):
#     @http.route('/de_sale_production_report/de_sale_production_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_production_report/de_sale_production_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_production_report.listing', {
#             'root': '/de_sale_production_report/de_sale_production_report',
#             'objects': http.request.env['de_sale_production_report.de_sale_production_report'].search([]),
#         })

#     @http.route('/de_sale_production_report/de_sale_production_report/objects/<model("de_sale_production_report.de_sale_production_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_production_report.object', {
#             'object': obj
#         })
