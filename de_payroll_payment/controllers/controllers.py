# -*- coding: utf-8 -*-
# from odoo import http


# class DePayrollPayment(http.Controller):
#     @http.route('/de_payroll_payment/de_payroll_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payroll_payment/de_payroll_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payroll_payment.listing', {
#             'root': '/de_payroll_payment/de_payroll_payment',
#             'objects': http.request.env['de_payroll_payment.de_payroll_payment'].search([]),
#         })

#     @http.route('/de_payroll_payment/de_payroll_payment/objects/<model("de_payroll_payment.de_payroll_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payroll_payment.object', {
#             'object': obj
#         })
