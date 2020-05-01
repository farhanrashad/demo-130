from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class Joborder(models.Model):
    _name = 'order.job'
    _description = 'this is job order model'

    def get_sub_task_count(self):
        count = self.env['projects.projects'].search_count([])
        self.sub_task = count

    def get_notes_count(self):
        count = self.env['projects.projects'].search_count([])
        self.notes_ad = count

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False)])

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain

        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    name = fields.Char()
    sub_task = fields.Integer(compute='get_sub_task_count')
    notes_ad = fields.Integer(compute='get_notes_count')
    active = fields.Boolean(string='Active', default=True)
    project_id = fields.Many2one('projects.projects', string='Project', default=lambda self: self.env.context.get('default_project_id'))
    customer_name = fields.Many2one('res.partner', string='Customer')
    assign_to = fields.Many2one('res.users', string='Assign to')
    starting_date = fields.Date(strinng='Starting Date')
    ending_date = fields.Date(string='Ending Date')
    deadline = fields.Date(string='Deadline')
    tags = fields.Many2many('res.company', string='Tags')
    material_planning = fields.One2many('order.job.linea', 'ref_order_job')
    stock_move_tab = fields.One2many('order.job.linesm', 'ref_stock_move')
    sub_task_tab = fields.One2many('order.job.linesubtask', 'ref_sub_task')
    sub_time_sheet = fields.One2many('order.job.linetimesheet', 'ref_time_sheet')
    stage_id = fields.Many2one('project.task.type', string='Stage', ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        domain="[('project_ids', '=', project_id)]", copy=False)

class Materialplanning(models.Model):
    _name = 'order.job.linea'
    _description = 'this is material planning model'

    # # @api.depends('unit_of_measure')
    # def set_unit_of_measure(self):
    #     for i in self:
    #         i.unit_of_measure = 'Unit(s)'

    product_name = fields.Many2one('product.product', string='Product')
    product_desc = fields.Char(string='Description')
    prod_quantity = fields.Integer(string='Quantity')
    unit_of_measure = fields.Char(string='Unit Of Measure', default='Unit(s)')
    ref_order_job = fields.Many2one('order.job', string='ref parent')


class Stockmove(models.Model):
    _name = 'order.job.linesm'
    _description = 'this is stock move model'

    expected_date = fields.Date(string='Expected Date')
    creation_date = fields.Date(string='Creation Date')
    source_document = fields.Char(string='Source Document')
    product_name = fields.Many2one('product.product', string='Product')
    initial_demand = fields.Integer(string='Initial Demand')
    unit_of_measure = fields.Char(string='Unit Of Measure', default='Unit(s)')
    state_check = fields.Char(string='State', default='done')
    ref_stock_move = fields.Many2one('order.job', string='ref parent')


class Subtasks(models.Model):
    _name = 'order.job.linesubtask'
    _description = 'this is sub task model'

    title = fields.Char(string='Title')
    project_subtask = fields.Many2one('projects.projects', string='Project')
    assign_to = fields.Many2one('res.users', string='Assign to')
    planned_hours = fields.Integer(string='Planned Hours')
    remaining_hours = fields.Integer(string='Remaining Hours')
    stage_subtask = fields.Char(string='Stage')
    progress = fields.Char(string='Progress')
    ref_sub_task = fields.Many2one('order.job', string='ref parent')

class Timesheet(models.Model):
    _name = 'order.job.linetimesheet'
    _description = 'this is time sheet model'

    date_tmeshet = fields.Date(string='Date')
    employee_name = fields.Many2one('res.users', string='Employee')
    description = fields.Text(string='Description')
    duration = fields.Float(string='Duration(Hours(s))')
    ref_time_sheet = fields.Many2one('order.job', string='ref parent')




class Notesjoborder(models.Model):
    _name = 'joborder.notes'
    _description = 'this is job order notes model'

    name = fields.Char(string='Name')
