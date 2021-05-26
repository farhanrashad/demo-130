from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class TravelRequest(models.Model):
    _name = 'travel.request'

    def unlink(self):
        for r in self:
            if r.state == 'refuse' or r.state == 'approved':
                raise UserError(
                    "Travel Request records which are set to Refuse/Approved can't be deleted!")
        return super(TravelRequest, self).unlink()

    @api.model
    def create(self, values):
        if values.get('travel_request', _('New')) == _('New'):
            values['travel_request'] = self.env['ir.sequence'].next_by_code('travel.request.travel_request') or _('New')
        return super(TravelRequest, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    travel_request = fields.Char('Name', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('refuse', 'Refuse'),
        ('approved', 'Approved'),
    ], string='State', index=True, copy=False, default='draft', track_visibility='onchange')

    def action_submit(self):
        self.state = 'submitted'

    def action_refuse(self):
        self.state = 'refuse'

    def action_approve(self):
        self.state = 'approved'

    name = fields.Char('Name')
    description = fields.Char('Description')
    travel_type = fields.Selection(
        [('business', 'Business'), ('personal', 'Personal'), ('visa run', 'Visa Run'), ('meeting', 'Meeting')],
        string="Travel Type", default="no")
    ticket_arr_paid = fields.Boolean('Ticket Arranged and Paid by IGT')
    duration = fields.Date('Duration')
    days = fields.Char('Days')
    employee_id = fields.Many2one('hr.employee', string="Employee", default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    designation_id = fields.Many2one('hr.job', string='designation', related='employee_id.job_id')
    nrc_other_id = fields.Char(string="NRC/Other ID", related="employee_id.identification_id")
    passport_no = fields.Char(string="Passport No", related="employee_id.passport_id")
    dob = fields.Date(string="Date of Birth", related="employee_id.birthday")
