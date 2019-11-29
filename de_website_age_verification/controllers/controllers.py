# -*- coding: utf-8 -*-
# from odoo import http


# class DeWebsiteAgeVerification(http.Controller):
#     @http.route('/de_website_age_verification/de_website_age_verification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_age_verification/de_website_age_verification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_age_verification.listing', {
#             'root': '/de_website_age_verification/de_website_age_verification',
#             'objects': http.request.env['de_website_age_verification.de_website_age_verification'].search([]),
#         })

#     @http.route('/de_website_age_verification/de_website_age_verification/objects/<model("de_website_age_verification.de_website_age_verification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_age_verification.object', {
#             'object': obj
#         })
