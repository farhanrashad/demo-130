# -*- coding: utf-8 -*-
# from odoo import http


# class DeHrEmployeeChecklist(http.Controller):
#     @http.route('/de_hr_employee_checklist/de_hr_employee_checklist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_hr_employee_checklist/de_hr_employee_checklist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_hr_employee_checklist.listing', {
#             'root': '/de_hr_employee_checklist/de_hr_employee_checklist',
#             'objects': http.request.env['de_hr_employee_checklist.de_hr_employee_checklist'].search([]),
#         })

#     @http.route('/de_hr_employee_checklist/de_hr_employee_checklist/objects/<model("de_hr_employee_checklist.de_hr_employee_checklist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_hr_employee_checklist.object', {
#             'object': obj
#         })
