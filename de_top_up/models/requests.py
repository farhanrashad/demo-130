from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class TopUpRequest(models.Model):
    _name = 'topup.request'
    _description = 'Top Up Request model'

    def unlink(self):
        for r in self:
            if r.state == 'approved' or r.state == 'cancelled' or r.state == 'distributed':
                raise UserError(
                    "TOPUP_Request records which are set to Approved/Cancelled/Distributed can't be deleted!")
        return super(TopUpRequest, self).unlink()

    @api.model
    def create(self, values):
        if values.get('topup_req', _('New')) == _('New'):
            values['topup_req'] = self.env['ir.sequence'].next_by_code('topup.request.emp_req') or _('New')
        return super(TopUpRequest, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    topup_req = fields.Char('REQ/2021/00001', required=True, copy=False, readonly=True, index=True,
                            default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('waiting for approval', 'Waiting For Approval'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
        ('distributed', 'Distributed')
    ], string='State', index=True, copy=False, default='draft', track_visibility='onchange')

    topup_request_lines = fields.One2many('topup.request.line', 'request_id')

    # @api.constrains('participants_ids')
    # def constraints_on_selection(self):
    #     if not self.participants_ids:
    #         raise UserError("Please select atleast 1 Employee!")

    def action_submitted(self):
        # flag = 0
        # for rec in self.participants_ids:
        #     flag = 1
        # if flag == 0:
        #     raise UserError("No participants added!")
        # else:
        self.state = 'waiting for approval'

    def action_approved(self):
        self.state = 'approved'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_distributed(self):
        # vals = {
        #     'name': self.name,
        #     'course_name': self.course,
        #     'institute': self.institute,
        #     'reason': self.reason,
        #     'participants_ids': self.participants_ids,
        #     'date_from': self.current_date,
        #     'date_to': self.end_date,
        #     'amount':self.training_cost
        # }
        #
        # result = self.env['employee.session'].create(vals)
        self.state = 'distributed'

    current_date = date.today()
    end_date = current_date + timedelta(days=30)

    description = fields.Text(String="Description")
    period = fields.Date(String="Period")
    requester = fields.Many2one('res.users', default=lambda self: self.env.user, String="Requester")
    department = fields.Many2one('hr.department', String="Department")
    representative_batch = fields.Selection(
        [('c-level', 'C-Level'), ('admin & fleet', 'Admin & Fleet'), ('documentation', 'Documentation'),
         ('engineering', 'Engineering'), ('accounting and finance', 'Accounting and Finance'),
         ('government relations and stakeholder engagement', 'Government Relations and Stakeholder Engagement'),
         ('human resources', 'Human Resources'), ('hse', 'HSE'), ('qa', 'QA'),
         ('information & technology', 'Information & Technology'), ('legal', 'Legal'),
         ('noc', 'NOC'),
         ('fields operations (north)', 'Fields Operations (North)'),
         ('fields operations (south)', 'Fields Operations (South)'), ('power', 'Power'),
         ('o&m rms', 'O&M RMS'), ('o&m support', 'O&M Support'), ('project management', 'Project Management'),
         ('rollout & colocation', 'Rollout & Colocation'), ('procurement', 'Procurement'),
         ('supply chain', 'Supply Chain')],
        String="Representative Batch")
    date = fields.Date(String="Date")
    type = fields.Selection([('employee benfit', 'Employee Benfit'), ('category use', 'Category Use')],
                            String="Type")
    is_level = fields.Boolean(String="Is C-Level")
    additional_req = fields.Boolean(String="Additional Request")


class EmployeeRequestLine(models.Model):
    _name = 'topup.request.line'
    _description = 'Top Up Request model'

    request_id = fields.Many2one('topup.request')

    employee = fields.Many2one('hr.employee', string="Employee")
    department = fields.Many2one('hr.department', string="Department", related="employee.department_id")
    telenor = fields.Integer(string="Telenor")
    ooredoo = fields.Integer(string="Ooredoo")
    mpt = fields.Integer(string="MPT")
    mytel = fields.Integer(string="MYTEL")
    total = fields.Integer(string="Total", computed="")
    remarks = fields.Char(string="Remarks")
