from odoo import models, fields, api


class Joborder(models.Model):
    _name = 'order.job'
    _description = 'this is job order model'

    def get_sub_task_count(self):
        count = self.env['projects.projects'].search_count([])
        self.sub_task = count

    def get_notes_count(self):
        count = self.env['projects.projects'].search_count([])
        self.notes_ad = count

    name = fields.Char()
    sub_task = fields.Integer(compute='get_sub_task_count')
    notes_ad = fields.Integer(compute='get_notes_count')
    active = fields.Boolean(string='Active', default=True)
    project_name = fields.Many2one('projects.projects', string='Project')
    customer_name = fields.Many2one('res.partner', string='Customer')
    assign_to = fields.Many2one('res.users', string='Assign to')
    starting_date = fields.Date(strinng='Starting Date')
    ending_date = fields.Date(string='Ending Date')
    deadline = fields.Date(string='Deadline')
    tags = fields.Many2one('res.company', string='Tags')
    material_planning = fields.One2many('order.job.linea', 'ref_order_job')
    stock_move_tab = fields.One2many('order.job.linesm', 'ref_stock_move')
    sub_task_tab = fields.One2many('order.job.linesubtask', 'ref_sub_task')


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


class Notesjoborder(models.Model):
    _name = 'joborder.notes'
    _description = 'this is job order notes model'

    name = fields.Char(string='Name')
