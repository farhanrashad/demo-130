from odoo import http
from odoo.http import request
from datetime import datetime
from odoo.addons.website_sale.controllers.main import WebsiteSale


def advance_salary_page_content():
    payment_methods = request.env['account.journal'].search([])
    employees = request.env['hr.employee'].search([])
    users = request.env['res.users'].search([])
    default_user_id = request.env.user.id
    print('user', request.env.user.id)
    login_user = request.env['res.users'].search([('id', '=', request.env.user.id)])
    email = login_user.login
    return {
        'payment_methods': payment_methods,
        'employees': employees,
        'users': users,
        'default_user_id': default_user_id,
        'email': email
    }


class MyAdvanceSalary(http.Controller):

    @http.route('/advance_salary_page', type="http", auth="user", website=True)
    def leave_template(self, **kw):
        print("Execution Here.........................")
        return http.request.render('de_employee_advance_salary.advance_salary_template', advance_salary_page_content())


    @http.route('/create/advancesalary', type="http", auth="public", website=True)
    def create_leave(self, **kw):
        fmt = '%Y-%m-%d'
        date_from = kw.get('request_date_from')
#         date_to = kw.get('request_date_to')
#         d1 = datetime.strptime(date_from, fmt)
#         d2 = datetime.strptime(date_to, fmt)
#         days_diff = float((d2 - d1).days)
        adv_sal_val = {
            'name': kw.get('name'),
            'employee_id': int(kw.get('employee_id')),
            'request_date': kw.get('request_date_from'),
            'amount': kw.get('request_date_to'),
            'emp_partner_id': kw.get('emp_partner_id'),
            'payment_method':kw.get('payment_method'),
            'note':kw.get('note'),
#             'user_id': request.env.user.id,
        }
        adv_sal_record = request.env['hr.employee.advance.salary'].sudo().create(adv_sal_val)
        return request.render("de_employee_advance_salary.adv_salary_thanks", {})