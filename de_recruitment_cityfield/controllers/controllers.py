# -*- coding: utf-8 -*-
# from odoo import http


# class DeRecruitmentCityfield(http.Controller):
#     @http.route('/de_recruitment_cityfield/de_recruitment_cityfield/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_recruitment_cityfield/de_recruitment_cityfield/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_recruitment_cityfield.listing', {
#             'root': '/de_recruitment_cityfield/de_recruitment_cityfield',
#             'objects': http.request.env['de_recruitment_cityfield.de_recruitment_cityfield'].search([]),
#         })

#     @http.route('/de_recruitment_cityfield/de_recruitment_cityfield/objects/<model("de_recruitment_cityfield.de_recruitment_cityfield"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_recruitment_cityfield.object', {
#             'object': obj
#         })
