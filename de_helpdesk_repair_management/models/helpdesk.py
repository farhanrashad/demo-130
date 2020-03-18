# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    project_id = fields.Many2one("project.project", string="Project", domain="[('allow_timesheets', '=', True), ('company_id', '=', company_id)]")
    
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=False, help="The analytic account related to a Ticket", copy=False,)
    

    diagnosys_count = fields.Integer('diagnosys Count', compute='_compute_diagnosys_count', compute_sudo=True)
    diagnosys_ids = fields.One2many('project.task', 'ticket_id', string='diagnosys')
    
    workorder_count = fields.Integer('workorder Count', compute='_compute_workorder_count', compute_sudo=True)
    workorder_ids = fields.One2many('project.task', 'ticket_id', string='Work Orders')

    @api.depends('diagnosys_ids')
    def _compute_diagnosys_count(self):
        diagnosys_data = self.env['project.task'].sudo().read_group([('ticket_id', 'in', self.ids),('is_diagnosys','=',True)], ['ticket_id'], ['ticket_id'])
        mapped_data = dict([(r['ticket_id'][0], r['ticket_id_count']) for r in diagnosys_data])
        for ticket in self:
            ticket.diagnosys_count = mapped_data.get(ticket.id, 0)

    def action_view_diagnosys(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('diagnosys'),
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('ticket_id', '=', self.id),('is_diagnosys','=',True)],
            'context': dict(self._context, create=False, default_company_id=self.company_id.id, default_ticket_id=self.id,default_partner_id=self.partner_id.id,default_is_diagnosys=True),
        }
    
    @api.depends('workorder_ids')
    def _compute_workorder_count(self):
        workorder_data = self.env['project.task'].sudo().read_group([('ticket_id', 'in', self.ids),('is_workorder','=',True)], ['ticket_id'], ['ticket_id'])
        mapped_data = dict([(r['ticket_id'][0], r['ticket_id_count']) for r in workorder_data])
        for ticket in self:
            ticket.workorder_count = mapped_data.get(ticket.id, 0)

    def action_view_workorder(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('workorder'),
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'domain': [('ticket_id', '=', self.id),('is_workorder','=',True)],
            'context': dict(self._context, create=False, default_company_id=self.company_id.id, default_ticket_id=self.id,default_partner_id=self.partner_id.id,default_is_workorder=True),
        }
