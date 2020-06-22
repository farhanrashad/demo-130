# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployee(http.Controller):
#     @http.route('/de_employee/de_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee/de_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee.listing', {
#             'root': '/de_employee/de_employee',
#             'objects': http.request.env['de_employee.de_employee'].search([]),
#         })

#     @http.route('/de_employee/de_employee/objects/<model("de_employee.de_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee.object', {
#             'object': obj
#         })
