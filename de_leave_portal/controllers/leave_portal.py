# # -*- coding: utf-8 -*-
from collections import OrderedDict
from operator import itemgetter
from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
from odoo.exceptions import UserError
from odoo.osv.expression import OR

def approval_page_content(flag = 0):
    partner = request.env['res.partner'].search([])
    category = request.env['approval.category'].search([])

    return {
        'approval_data': category,
        'oweners_res_partner' : partner,
        'success_flag' : flag
    }
 
class CreateApproval(http.Controller):

    @http.route('/approval/create/',type="http", website=True, auth='user')
    def approvals_create_template(self, **kw):
        return request.render("de_approval_portal.create_approval",approval_page_content()) 
    
    @http.route('/my/approval/save', type="http", auth="public", website=True)
    def create_approvals(self, **kw):
        approval_val = {
            'name': kw.get('approval_name'),
            'has_location': kw.get('approval_has_loc'),
            'category_id': int(kw.get('approval_category_id')),
#             'date_start':'date_start',
#             'date_end': 'date_end',
        }
        record = request.env['approval.request'].sudo().create(approval_val)

        success_flag = 1
        return request.render("de_approval_portal.create_approval", approval_page_content(success_flag))

class ActionApproval(CustomerPortal):
        
    @http.route(['/approval/accept/<int:approval_id>'], type='http', auth="public", website=True)
    def accept_approval(self,approval_id ,**kw):
        id=approval_id
        recrd = request.env['approval.request'].sudo().browse(id)
        recrd.action_approve()
        approvals_page = CustomerPortal()
        return approvals_page.portal_my_approvals()
        
    @http.route(['/approval/reject/<int:approval_id>'], type='http', auth="public", website=True)
    def reject_approval(self,approval_id ,**kw):
        id=approval_id
        recrd = request.env['approval.request'].sudo().browse(id)
        recrd.action_refuse()
        approvals_page = CustomerPortal()
        return approvals_page.portal_my_approvals()   
        
    @http.route(['/app/rjct/<int:approval_id>'], type='http', auth="public", website=True)
    def reject_rjct(self,approval_id , access_token=None, **kw):
        id=approval_id
        record = request.env['approval.request'].sudo().browse(id)
#         if record.request_status != 'approved': 
#             record.action_refuse()
        record.action_refuse()
        try:
            approval_sudo = self._document_check_access('approval.request', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._approval_get_page_view_values(approval_sudo, **kw) 
        return request.render("de_approval_portal.portal_my_approval", values)
        
        
    @http.route(['/app/ccpt/<int:approval_id>'], type='http', auth="public", website=True)
    def reject_ccpt(self,approval_id , access_token=None, **kw):
        id=approval_id
        recrd = request.env['approval.request'].sudo().browse(id)
#         if recrd.request_status != 'refused': 
#             recrd.action_approve()
        recrd.action_approve()
        try:
            approval_sudo = self._document_check_access('approval.request', id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        values = self._approval_get_page_view_values(approval_sudo, **kw) 
        return request.render("de_approval_portal.portal_my_approval", values)


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'approval_count' in counters:
            values['approval_count'] = request.env['approval.request'].search_count([])
        return values
  
    
    def _approval_get_page_view_values(self, approval, approver_user_flag = 0,access_token = None, **kwargs):
        values = {
            'page_name': 'approval',
            'approval': approval,
            'approver_user_flag':approver_user_flag,
        }
        return self._get_page_view_values(approval, access_token, values, 'my_approvals_history', False, **kwargs)
    

    @http.route(['/my/approvals', '/my/approvals/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_approvals(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None,
                         search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name' },
            'update': {'label': _('Last Update'), 'order': 'write_date desc'},
        }
        
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': [('request_status', 'in', ['new', 'pending','approved','refused','cancel'])]},
            'new': {'label': _('To Submit'), 'domain': [('request_status', '=', 'new')]},
            'pending': {'label': _('Submitted'), 'domain': [('request_status', '=', 'pending')]},  
            'approved': {'label': _('Approved'), 'domain': [('request_status', '=', 'approved')]},
            'refused': {'label': _('Refused'), 'domain': [('request_status', '=', 'refused')]}, 
            'cancel': {'label': _('Cancel'), 'domain': [('request_status', '=', 'cancel')]},
        }
   
        
        searchbar_inputs = {
            
            'name': {'input': 'name', 'label': _('Search in Name')},
#             'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'reason': {'input': 'reason', 'label': _('Search in Description')},
            'id': {'input': 'id', 'label': _('Search in Ref#')},
            'category_id.name': {'input': 'category_id.name', 'label': _('Search in Category')},
            'request_owner_id.name': {'input': 'request_owner_id.name', 'label': _('Search in Request Owner')},
            'partner_id.name': {'input': 'partner_id.name', 'label': _('Search in Contact')},
            'request_status': {'input': 'request_status', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
        }

        project_groups = request.env['approval.request'].search([])

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]       

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('name', 'all'):
                search_domain = OR([search_domain, [('name', 'ilike', search)]])
            if search_in in ('id', 'all'):
                search_domain = OR([search_domain, [('id', 'ilike', search)]])
            if search_in in ('reason', 'all'):
                search_domain = OR([search_domain, [('reason', 'ilike', search)]])
            if search_in in ('category_id.name', 'all'):
                search_domain = OR([search_domain, [('category_id.name', 'ilike', search)]])
            if search_in in ('request_owner_id.name', 'all'):
                search_domain = OR([search_domain, [('request_owner_id.name', 'ilike', search)]])
            if search_in in ('partner_id.name', 'all'):
                search_domain = OR([search_domain, [('partner_id.name', 'ilike', search)]])
            if search_in in ('request_status', 'all'):
                search_domain = OR([search_domain, [('request_status', 'ilike', search)]])
            domain += search_domain
 
        approval_count = request.env['approval.request'].search_count(domain)

        # pager
        pager = portal_pager(
            url="/my/Approvals",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby,
                      'seissuesarch_in': search_in, 'search': search},
            total=approval_count,
            page=page,
            step=self._items_per_page
        )

        _approvals = request.env['approval.request'].search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_approvals_history'] = _approvals.ids[:100]

        grouped_approvals = [_approvals]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_approvals': grouped_approvals,
            'page_name': 'approval',
            'default_url': '/my/approvals',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
        })
        return request.render("de_approval_portal.portal_my_approvals", values)   

   
    @http.route(['/my/approval/<int:approval_id>'], type='http', auth="user", website=True)
    def portal_my_approval(self, approval_id, access_token=None, **kw):
        values = []
        active_user = http.request.env.context.get('uid')
        approver_user = []
        id = approval_id
        try:
            approval_sudo = self._document_check_access('approval.request', approval_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        
        record = request.env['approval.request'].sudo().browse(id)
        for aprover in record.approver_ids:
            approver_user.append(aprover.user_id.id)
        approver_user_flag = 0
        for user in  approver_user:
            if user == active_user:
                approver_user_flag = 1
#         raise UserError((approver_user_flag))
        values = self._approval_get_page_view_values(approval_sudo, approver_user_flag,access_token, **kw) 
        return request.render("de_approval_portal.portal_my_approval", values)

    