# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class ProjectTaskType(models.Model):
    _name = 'project.task.type'
    _description = 'Task Stage'
    _order = 'sequence, id'

    def _get_default_project_ids(self):
        default_project_id = self.env.context.get('default_project_id')
        return [default_project_id] if default_project_id else None

    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(translate=True)
    sequence = fields.Integer(default=1)
    project_ids = fields.Many2many('projects.projects', 'project_task_type_rel', 'type_id', 'project_id', string='Projects',
        default=_get_default_project_ids)
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Ready for Next Stage'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    mail_template_id = fields.Many2one(
        'mail.template',
        string='Email Template',
        domain=[('model', '=', 'project.task')],
        help="If set an email will be sent to the customer when the task or issue reaches this step.")
    fold = fields.Boolean(string='Folded in Kanban',
        help='This stage is folded in the kanban view when there are no records in that stage to display.')
    rating_template_id = fields.Many2one(
        'mail.template',
        string='Rating Email Template',
        domain=[('model', '=', 'project.task')],
        help="If set and if the project's rating configuration is 'Rating when changing stage', then an email will be sent to the customer when the task reaches this step.")
    auto_validation_kanban_state = fields.Boolean('Automatic kanban status', default=False,
        help="Automatically modify the kanban state when the customer replies to the feedback for this stage.\n"
            " * A good feedback from the customer will update the kanban state to 'ready for the new stage' (green bullet).\n"
            " * A medium or a bad feedback will set the kanban state to 'blocked' (red bullet).\n")

    def unlink(self):
        stages = self
        default_project_id = self.env.context.get('default_project_id')
        if default_project_id:
            shared_stages = self.filtered(lambda x: len(x.project_ids) > 1 and default_project_id in x.project_ids.ids)
            tasks = self.env['project.task'].with_context(active_test=False).search([('project_id', '=', default_project_id), ('stage_id', 'in', self.ids)])
            if shared_stages and not tasks:
                shared_stages.write({'project_ids': [(3, default_project_id)]})
                stages = self.filtered(lambda x: x not in shared_stages)
        return super(ProjectTaskType, stages).unlink()





class Projectcons(models.Model):
    _name = 'projects.projects'
    # _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']
    _description = 'this is project model'

    def action_share(self):
        print('world')

    def _compute_task_count(self):
        task_data = self.env['order.job'].read_group(
            [('project_id', 'in', self.ids), '|', ('stage_id.fold', '=', False), ('stage_id', '=', False)],
            ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.task_count = result.get(project.id, 0)

    # ('class_student', '=', self.id)
    def get_document_count(self):
        count = self.env['projects.projects'].search_count([])
        self.documents_count = count

    def get_task_count(self):
        count = self.env['projects.projects'].search_count([])
        self.task_count = count

    def get_notes_count(self):
        count = self.env['projects.projects'].search_count([])
        self.notes_count = count

    def _compute_is_favorite(self):
        for project in self:
            project.is_favorite = self.env.user in project.favorite_user_ids

    def _inverse_is_favorite(self):
        favorite_projects = not_fav_projects = self.env['projects.projects'].sudo()
        for project in self:
            if self.env.user in project.favorite_user_ids:
                favorite_projects |= project
            else:
                not_fav_projects |= project

        # Project User has no write access for project.
        not_fav_projects.write({'favorite_user_ids': [(4, self.env.uid)]})
        favorite_projects.write({'favorite_user_ids': [(3, self.env.uid)]})

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    # @api.depends('visibility')
    # def set_default_value(self):
    #     for i in self:
    #         i.visibility = 'All employees'

    # type_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', string='Tasks Stages')
    rating_status = fields.Selection(
        [('stage', 'Rating when changing stage'), ('periodic', 'Periodical Rating'), ('no', 'No rating')],
        'Customer(s) Ratings', help="How to get customer feedback?\n"
                                    "- Rating when changing stage: an email will be sent when a task is pulled in another stage.\n"
                                    "- Periodical Rating: email will be sent periodically.\n\n"
                                    "Don't forget to set up the mail templates on the stages for which you want to get the customer's feedbacks.",
        default="no", required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", copy=False,
                                          ondelete='set null',
                                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                          check_company=True,
                                          help="Analytic account to which this project is linked for financial management. "
                                               "Use an analytic account to record cost and revenue on your project.")
    # favorite_user_ids = fields.Many2many(
    #     'res.users', 'project_favorite_user_rel', 'project_id', 'user_id',
    #     default=_get_default_favorite_user_ids,
    #     string='Members')
    is_favorite = fields.Boolean(compute='_compute_is_favorite', inverse='_inverse_is_favorite', string='Show Project on dashboard',
    alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=True,
        help="Internal email associated with this project. Incoming emails are automatically synchronized "
             "with Tasks (or optionally Issues if the Issue Tracker module is installed)."))
    label_tasks = fields.Char(string='Use Tasks as', default='Tasks', help="Label used for the tasks of the project.")
    name = fields.Char(string='Name', bold=True)
    task_name = fields.Char(string='Name of tasks:')
    # projects_projects_linea = fields.One2many('projects.projects.linea', 'sub_task_project', string='settings')
    documents_count = fields.Integer(compute='get_document_count')
    task_count = fields.Integer(compute='get_task_count')
    notes_count = fields.Integer(compute='get_notes_count')

    project_manager = fields.Many2one('res.users', string='Project Manager')
    partner_id = fields.Many2one('res.partner', string='Customer', auto_join=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    user_id = fields.Many2one('res.users', string='Project Manager', default=lambda self: self.env.user, tracking=True)

    image_hr = fields.Binary('image')
    customer_name = fields.Many2one('res.partner', string='customer')
    # analytic_account = fields.
    visibility = fields.Selection([('invited_employee', 'Invited employee'),
                                   ('all_employee', 'All eemployee'),
                                   ('portal_user','Portal user')],'Visibility')
    sub_task_project = fields.Many2one('projects.projects', string='Sub-task Project')
    company = fields.Many2one('res.company', string='Company')
    timesheet_f = fields.Boolean(string='Timesheet' , store=True)
    customer_rating = fields.Selection([('changing_stage', 'Rating When changing stage'),
                                   ('all_employee', 'Periodicaly Rating'),
                                   ('portal_user', 'No rating')],'Customer Ratings')
    construction_site = fields.Selection([('agriculture', 'Agriculture'),
                                        ('residential', 'Residential'),
                                        ('commercial', 'Commertial')] ,'Type of Construction')
    construction_location = fields.Char(string='Location')
    active = fields.Boolean(default=True,
                            help="If the active field is set to False, it will allow you to hide the project without removing it.")
    displayed_image_id = fields.Many2one('ir.attachment', domain="[('res_model', '=', 'order.job'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]", string='Cover Image')
    color = fields.Integer(string='Color Index')
    task_count = fields.Integer(compute='_compute_task_count', string="Task Count")

    # time_schedule=fields.Many2one('timesh')
    @api.model
    def activate_sample_project(self):
        """ Unarchives the sample project 'project.project_project_data' and
            reloads the project dashboard """
        # Unarchive sample project
        project = self.env.ref('de_construction_app.projects_projects_data', False)
        if project:
            project.write({'active': True})

        cover_image = self.env.ref('de_construction_app.msg_task_data_14_attach', False)
        cover_task = self.env.ref('de_construction_app.order_job_data_14', False)
        if cover_image and cover_task:
            cover_task.write({'displayed_image_id': cover_image.id})

        # Change the help message on the action (no more activate project)
        action = self.env.ref('de_construction_app.open_view_project_all', False)
        action_data = None
        if action:
            action.sudo().write({
                "help": _('''<p class="o_view_nocontent_smiling_face">
                      Create a new project</p>''')
            })
            action_data = action.read()[0]
        # Reload the dashboard
        return action_data

    def open_tasks(self):
        ctx = dict(self._context)
        ctx.update({'search_default_project_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('de_construction_app', 'act_project_project_2_project_task_all')
        return dict(action, context=ctx)

    # def _compute_is_favorite(self):
    #     for project in self:
    #         project.is_favorite = self.env.user in project.favorite_user_ids


class Projectlineitem(models.Model):
    _name = 'projects.projects.linea'
    _description = 'this is project line table'




class Projectcons(models.Model):
    _name = 'notes.notes'
    _description = 'this is project model'
    _rec_name = 'tes_note'

    tags_note = fields.Char(string='Tags')
    task_job_order = fields.Many2one('order.job',string='Task/ Job Order')
    construction_projecct = fields.Many2one('projects.projects',string='Construction Project')
    responsible_user = fields.Many2one('res.users',string='Responsible User')
    tes_note = fields.Text()
    state = fields.Selection([
        ('new', 'New'),
        ('meeting_mint', 'Meeting Minutes'),
        ('notes', 'Notes'),
        ('todo', 'Todo'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='new')
