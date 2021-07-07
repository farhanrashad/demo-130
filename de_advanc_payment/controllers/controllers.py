# -*- coding: utf-8 -*-
# from odoo import http


# class DeAdvancPayment(http.Controller):
#     @http.route('/de_advanc_payment/de_advanc_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_advanc_payment/de_advanc_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_advanc_payment.listing', {
#             'root': '/de_advanc_payment/de_advanc_payment',
#             'objects': http.request.env['de_advanc_payment.de_advanc_payment'].search([]),
#         })

#     @http.route('/de_advanc_payment/de_advanc_payment/objects/<model("de_advanc_payment.de_advanc_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_advanc_payment.object', {
#             'object': obj
#         })
