# -*- coding: utf-8 -*-
# from odoo import http


# class DeStockPickingReport(http.Controller):
#     @http.route('/de_stock_picking_report/de_stock_picking_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_stock_picking_report/de_stock_picking_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_stock_picking_report.listing', {
#             'root': '/de_stock_picking_report/de_stock_picking_report',
#             'objects': http.request.env['de_stock_picking_report.de_stock_picking_report'].search([]),
#         })

#     @http.route('/de_stock_picking_report/de_stock_picking_report/objects/<model("de_stock_picking_report.de_stock_picking_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_stock_picking_report.object', {
#             'object': obj
#         })
