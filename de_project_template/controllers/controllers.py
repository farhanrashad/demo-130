# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectTemplate(http.Controller):
#     @http.route('/de_project_template/de_project_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_template/de_project_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_template.listing', {
#             'root': '/de_project_template/de_project_template',
#             'objects': http.request.env['de_project_template.de_project_template'].search([]),
#         })

#     @http.route('/de_project_template/de_project_template/objects/<model("de_project_template.de_project_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_template.object', {
#             'object': obj
#         })
