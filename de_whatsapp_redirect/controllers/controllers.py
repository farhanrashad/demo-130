# -*- coding: utf-8 -*-
# from odoo import http


# class DeSendWhatsappMessage(http.Controller):
#     @http.route('/de_whatsapp_redirect/de_whatsapp_redirect/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_whatsapp_redirect/de_whatsapp_redirect/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_whatsapp_redirect.listing', {
#             'root': '/de_whatsapp_redirect/de_whatsapp_redirect',
#             'objects': http.request.env['de_whatsapp_redirect.de_whatsapp_redirect'].search([]),
#         })

#     @http.route('/de_whatsapp_redirect/de_whatsapp_redirect/objects/<model("de_whatsapp_redirect.de_whatsapp_redirect"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_whatsapp_redirect.object', {
#             'object': obj
#         })
