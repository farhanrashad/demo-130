from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def compute_pending_approval(self):
        for request in self:
            approval_request = self.env['approval.request'].search([('id', '=', request.approval_request_id.id)])
            if approval_request.approver_ids:
                for line in approval_request.approver_ids:
                    if line.is_pending == True:
                        request.is_approval_pending = True
                        break
                    if line.is_pending == False and line.status == 'approved':
                        request.is_approval_pending = False
                    else:
                        request.is_approval_pending = True
            else:
                request.is_approval_pending = True

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting for Approval'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    is_approval_pending = fields.Boolean('Approval Pending', default=True, compute='compute_pending_approval')
    approval_request = fields.Many2one('approval.category', domain=[('is_invoice', '=', True)], string='Approval Type')
    approval_request_id = fields.Many2one('approval.request')
    approver_count = fields.Integer(compute='_approver_count', string='No. of Approvers')

    def _approver_count(self):
        approval_category = self.env['approval.request'].search([('id', '=', self.approval_request_id.id)])
        count = 0
        for line in approval_category.approver_ids:
            count += 1
        self.approver_count = count

    def button_approval(self):
        category = ''
        for request in self:
            req_id = self.env['approval.request'].create({
                'name': request.name,
                'request_owner_id': self.env.user.id,
                'category_id': self.approval_request.id,
                'invoice_id': self.id,
            })
            request.approval_request_id = req_id.id
            req_id.action_confirm()

        self.write({'state': 'waiting'})

    def action_open_approvals(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("approvals.approval_request_action_all")
        action['domain'] = [('id', '=', self.approval_request_id.id)]
        return action


class ApprovalCategoryInherited(models.Model):
    _inherit = 'approval.category'

    is_invoice = fields.Boolean('PO', default=False)


class ApprovalRequestInherit(models.Model):
    _inherit = 'approval.request'

    invoice_id = fields.Many2one('purchase.order')

    def action_open_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Order'),
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('id', '=', self.invoice_id.id)],
            'context': dict(self._context, create=False),
        }
