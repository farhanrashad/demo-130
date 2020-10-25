# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MomCalendar(models.Model):
    _inherit = 'calendar.event'

    def print_mom(self):
        return self.env.ref('de_mom.mom_print_pdf_report').report_action(self)

    def action_send_mail(self):
        for rec in self:
            template_id = rec.env.ref('de_mom.mom_email_template_id').id
            template = rec.env['mail.template'].browse(template_id)
            template.send_mail(rec.id, force_send=True)

    project_id = fields.Many2one('project.project', string='Project')
    mom_meetings_ids = fields.One2many('mom.meetings.inherit', 'mom_task_id', string='Meetings')
    discussion = fields.Html(string='Discussion', copy=False)
    action_items = fields.Html(string='Action Items', copy=False)


class MomMeetings(models.Model):
    _name = 'mom.meetings.inherit'
    _description = 'This is meeting module extension'

    task_id = fields.Many2one('project.task', string='Task', required=True)
    name = fields.Char(related='task_id.name', string='Name')
    stage_id = fields.Many2one(related='task_id.stage_id', string='Stage')
    user_id = fields.Many2one(related='task_id.user_id', string='Assigned To')
    description = fields.Html(related='task_id.description', string='Description', readonly=False)
    deadline = fields.Date(related='task_id.date_deadline', string='Deadline', readonly=False)
    mom_task_id = fields.Many2one('calendar.event', string='Tasks')
