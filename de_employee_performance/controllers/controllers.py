# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeePerformance(http.Controller):
#     @http.route('/de_employee_performance/de_employee_performance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_performance/de_employee_performance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_performance.listing', {
#             'root': '/de_employee_performance/de_employee_performance',
#             'objects': http.request.env['de_employee_performance.de_employee_performance'].search([]),
#         })

#     @http.route('/de_employee_performance/de_employee_performance/objects/<model("de_employee_performance.de_employee_performance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_performance.object', {
#             'object': obj
#         })
