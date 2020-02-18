# -*- coding: utf-8 -*-
# from odoo import http


# class DePaymentWorkflow(http.Controller):
#     @http.route('/de_payment_workflow/de_payment_workflow/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payment_workflow/de_payment_workflow/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payment_workflow.listing', {
#             'root': '/de_payment_workflow/de_payment_workflow',
#             'objects': http.request.env['de_payment_workflow.de_payment_workflow'].search([]),
#         })

#     @http.route('/de_payment_workflow/de_payment_workflow/objects/<model("de_payment_workflow.de_payment_workflow"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payment_workflow.object', {
#             'object': obj
#         })
