from odoo import models, fields, api


class ProjectTemplate(models.Model):
    _inherit = 'project.project'

    is_project_template = fields.Boolean(default=False)

    def action_create_project(self):

        rec = self.env['project.project'].create({
            'name': self.name,
            'label_tasks': self.label_tasks,
            # 'user_id': self.user_id.id,
            'partner_id': self.partner_id.id,
            'privacy_visibility': self.privacy_visibility,
            'resource_calendar_id': self.resource_calendar_id.id,
            'is_project_template': False,
        })

        project_tasks = self.env['project.task'].search([('project_id', '=', self.id)])
        for task in project_tasks:
            self.env['project.task'].create({
                'name': task.name,
                'project_id': rec.id,
                'user_id': task.user_id.id,
                'task_id': task.task_id,
                'issue_type': task.issue_type.id,
                'date_deadline': task.date_deadline,
                'tag_ids': task.tag_ids,
                'description': task.description,
                'environment': task.environment,
            })

        form_id = self.env.ref('project.edit_project', False)
        return {
            'name': 'Project Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'view_id': form_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': rec.id,
            'context': {'force_detailed_view': 'true'},
        }

    def action_create_project_template(self):
        rec = self.env['project.project'].create({
            'name': self.name,
            'label_tasks': self.label_tasks,
            # 'user_id': self.user_id.id,
            'partner_id': self.partner_id.id,
            'privacy_visibility': self.privacy_visibility,
            'resource_calendar_id': self.resource_calendar_id.id,
            'is_project_template': True
        })

        project_tasks = self.env['project.task'].search([('project_id', '=', self.id)])
        for task in project_tasks:
            self.env['project.task'].create({
                'name': task.name,
                'project_id': rec.id,
                'user_id': task.user_id.id,
                'task_id': task.task_id,
                'issue_type': task.issue_type.id,
                'date_deadline': task.date_deadline,
                'tag_ids': task.tag_ids,
                'description': task.description,
                'environment': task.environment,
            })

        form_id = self.env.ref('project.edit_project', False)
        return {
            'name': 'Project Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.project',
            'view_id': form_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': rec.id,
            'context': {'force_detailed_view': 'true'},
        }


class TaskTemplate(models.Model):
    _inherit = 'project.task'

    is_task_template = fields.Boolean(default=False)

    def action_create_task(self):
        rec = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'user_id': self.user_id.id,
            'task_id': self.task_id,
            'issue_type': self.issue_type.id,
            'date_deadline': self.date_deadline,
            'tag_ids': self.tag_ids,
            'description': self.description,
            'environment': self.environment,
            'is_task_template': False,
        })
        form_id = self.env.ref('project.view_task_form2', False)
        return {
            'name': 'Project Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'view_id': form_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': rec.id,
            'context': {'force_detailed_view': 'true'},
        }

    def action_create_task_template(self):
        rec = self.env['project.task'].create({
            'name': self.name,
            'project_id': self.project_id.id,
            'user_id': self.user_id.id,
            'task_id': self.task_id,
            'issue_type': self.issue_type.id,
            'date_deadline': self.date_deadline,
            'tag_ids': self.tag_ids,
            'description': self.description,
            'environment': self.environment,
            'is_task_template': True,
        })
        form_id = self.env.ref('project.view_task_form2', False)
        return {
            'name': 'Project Task',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'project.task',
            'view_id': form_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': rec.id,
            'context': {'force_detailed_view': 'true'},
        }
