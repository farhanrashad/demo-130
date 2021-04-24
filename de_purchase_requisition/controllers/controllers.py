# -*- coding: utf-8 -*-
# from odoo import http


# class DeMaterialRequisition(http.Controller):
#     @http.route('/de_material_requisition/de_material_requisition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_material_requisition/de_material_requisition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_material_requisition.listing', {
#             'root': '/de_material_requisition/de_material_requisition',
#             'objects': http.request.env['de_material_requisition.de_material_requisition'].search([]),
#         })

#     @http.route('/de_material_requisition/de_material_requisition/objects/<model("de_material_requisition.de_material_requisition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_material_requisition.object', {
#             'object': obj
#         })
