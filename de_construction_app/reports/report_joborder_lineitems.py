
from odoo import models, api, fields, _

class JobOrderreport(models.AbstractModel):
    _name= 'report.de_construction_app.report_order_job'
    _description = 'job order model'

    @api.model
    def _get_report_values(self, decides, data=None):
        docs=self.env['order.job'].browse(decides[0])
        materialsplanning = self.env['order.job.linea'].search([('ref_order_job' ,'=' ,decides[0])])
        subtask = self.env['order.job.linesubtask'].search([('ref_sub_task' ,'=' ,decides[0])])
        stockmove = self.env['order.job.linesm'].search([('ref_stock_move' ,'=' ,decides[0])])
        stockmove_list = []
        for i in stockmove:
            vals = {
                'expected_date': i.expected_date,
                'creation_date': i.creation_date,
                'source_document': i.source_document,
                'product_name': i.product_name,
                'initial_demand': i.initial_demand,
                'unit_of_measure': i.unit_of_measure,
                'state_check': i.state_check,
            }
            stockmove_list.append(vals)


        subtask_list = []
        for i in subtask:
            vals = {
                'title': i.title,
                'project_subtask': i.project_subtask,
                'assign_to': i.assign_to,
                'planned_hours': i.planned_hours,
                'remaining_hours': i.remaining_hours,
                'stage_subtask': i.stage_subtask,
            }
            subtask_list.append(vals)
            #material planning
        material_list = []
        for i in materialsplanning:
            vals = {
                'product_name': i.product_name,
                'product_desc': i.product_desc,
                'prod_quantity': i.prod_quantity,
                'unit_of_measure': i.unit_of_measure
            }
            material_list.append(vals)
        return{
            'doc_model': 'order.job',
            'data': data,
            'docs': docs,
            'material_list': material_list,
            'subtask_list': subtask_list,
            'stockmove_list': stockmove_list,
        }

