# import logging
# import werkzeug
# import odoo.http as http
# import base64
# from openerp.http import request
# _logger = logging.getLogger(__name__)
# 
# from odoo.addons.de_sale_warranty.controllers.main import WarrantyController
# 
# class WarrantyControllerSite(WarrantyController):
# 
#     @http.route('/ticket/close', type="http", auth="user")
#     def support_warranty_close(self, **kw):
#         """Close the support ticket"""
#         values = {}
#         for field_name, field_value in kw.items():
#             if field_name.endswith('_id'):
#                 values[field_name] = int(field_value)
#             else:
#                 values[field_name] = field_value
#         ticket = http.request.env['sales.warranty'].sudo().\
#             search([('id', '=', values['name'])])
#         ticket.stage_id = values.get('state')
# 
#         return werkzeug.utils.redirect("/my/ticket/" + str(ticket.id))
# 
#     @http.route('/new/ticket', type="http", auth="user", website=True)
#     def create_new_warranty(self, **kw):
#         categories = http.request.env['sales.warranty']. \
#             search([('active', '=', True)])
#         email = http.request.env.user.email
#         name = http.request.env.user.name
#         return http.request.render('de_sale_warranty.portal_create_ticket', {
#             'categories': categories, 'email': email, 'name': name})
# 
#     @http.route('/submitted/ticket',
#                 type="http", auth="user", website=True, csrf=True)
#     def submit_ticket(self, **kw):
#         vals = {
#             'partner_name': kw.get('name'),
#             'company_id': http.request.env.user.company_id.id,
#             'category_id': kw.get('category'),
#             'partner_email': kw.get('email'),
#             'reference': kw.get('reference'),
#             'site_name': kw.get('site_name'),
#             'contact_name': kw.get('contact_name'),
#             'site_address': kw.get('site_address'),
#             'city': kw.get('city'),
#             'material': kw.get('material'),
#             'barcode': kw.get('barcode'),
#             'model': kw.get('model'),
#             'description': kw.get('description'),
#             'name': kw.get('subject'),
#             'attachment_ids': False,
#             'channel_id':
#                 request.env['helpdesk.ticket.channel'].
#                 sudo().search([('name', '=', 'Web')]).id,
#             'partner_id':
#                 request.env['res.partner'].sudo().search([
#                     ('name', '=', kw.get('name')),
#                     ('email', '=', kw.get('email'))]).id
#         }
#         new_ticket = request.env['helpdesk.ticket'].sudo().create(
#             vals)
#         new_ticket.message_subscribe(
#             partner_ids=request.env.user.partner_id.ids)
#         if kw.get('attachment'):
#             for c_file in request.httprequest.files.getlist('attachment'):
#                 data = c_file.read()
#                 if c_file.filename:
#                     request.env['ir.attachment'].sudo().create({
#                         'name': c_file.filename,
#                         'datas': base64.b64encode(data),
#                         #'datas_fname': c_file.filename,
#                         'res_model': 'helpdesk.ticket',
#                         'res_id': new_ticket.id
#                     })
#         return werkzeug.utils.redirect("/my/tickets")
