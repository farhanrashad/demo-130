# -*- coding: utf-8 -*-
# from odoo import http


# class DeTaskSubtaskChecklist(http.Controller):
#     @http.route('/de_task_subtask_checklist/de_task_subtask_checklist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_task_subtask_checklist/de_task_subtask_checklist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_task_subtask_checklist.listing', {
#             'root': '/de_task_subtask_checklist/de_task_subtask_checklist',
#             'objects': http.request.env['de_task_subtask_checklist.de_task_subtask_checklist'].search([]),
#         })

#     @http.route('/de_task_subtask_checklist/de_task_subtask_checklist/objects/<model("de_task_subtask_checklist.de_task_subtask_checklist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_task_subtask_checklist.object', {
#             'object': obj
#         })
