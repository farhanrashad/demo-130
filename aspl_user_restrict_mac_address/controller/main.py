# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

import odoo
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home, ensure_db
from odoo.tools.translate import _
from odoo import SUPERUSER_ID

class Home(Home):
    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                user_id = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
                mac_id = request.params['mac_address'] if request.params.get('mac_address') else False
                if user_id:
                    if user_id.id == 2 or not user_id.mac_address_restrict:
                        uid = request.session.authenticate(request.session.db, request.params['login'],
                                                           request.params['password'])
                        request.params['login_success'] = True
                        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                    elif not mac_id:
                        values['error'] = False
                        values['error'] = _("Please start your Node application or contact to administator")
                    elif mac_id in [mac.name for mac in user_id.allow_mac_ids]:
                        uid = request.session.authenticate(request.session.db, request.params['login'],
                                                           request.params['password'])
                        request.params['login_success'] = True
                        mac_id = False
                        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                    else:
                        request.params['login_success'] = False
                        values['error'] = False
                        values['error'] = _("You can not login with  "+mac_id+" address")
                else:
                    values['error'] = _("Wrong login/password")
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response