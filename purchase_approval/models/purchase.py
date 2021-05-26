# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('first_approval', 'First Approval'),
        ('second_approval', 'Second Approval'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    first_approval = fields.Boolean('First Approval', copy=False)
    second_approval = fields.Boolean('Second Approval', copy=False)
    is_approve_visible = fields.Boolean(compute='compute_is_approve_visible')

    def compute_is_approve_visible(self):
        for order in self:
            first_approver = self.env.user.has_group('purchase_approval.group_first_approval')
            second_approver = self.env.user.has_group('purchase_approval.group_second_approval')
            if order.state in ('first_approval', 'second_approval') and order.company_id.po_double_validation in ('one_step', 'two_step'):
                if order.company_id.po_double_validation == 'one_step' and (not order.first_approval and first_approver):
                    order.is_approve_visible = True
                else:
                    order.is_approve_visible = False
                if order.company_id.po_double_validation == 'two_step':
                    if (not order.first_approval and first_approver) or (not order.second_approval and second_approver):
                        order.is_approve_visible = True
                    else:
                        order.is_approve_visible = False
                if not first_approver and not second_approver:
                    order.is_approve_visible = False
            else:
                order.is_approve_visible = False

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.purchase_approval and order.company_id.po_double_validation in ('one_step', 'two_step'):
                order.write({'state': 'first_approval'})
            else:
                order.button_approve()
            # if order.company_id.po_double_validation == 'one_step'\
            #         or (order.company_id.po_double_validation == 'two_step'\
            #             and order.amount_total < self.env.company.currency_id._convert(
            #                 order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
            #         or order.user_has_groups('purchase.group_purchase_manager'):
            #     order.button_approve()
            # else:
            #     order.write({'state': 'to approve'})
        return True

    def button_approve(self, force=False):
        approved = False

        first_approver = self.user_has_groups('purchase_approval.group_first_approval')
        second_approver = self.user_has_groups('purchase_approval.group_second_approval')

        if self.company_id.purchase_approval and self.company_id.po_double_validation == 'one_step' and first_approver:
            approved = True
            self.write({'first_approval': True})

        if self.company_id.purchase_approval and self.company_id.po_double_validation == 'two_step':
            if first_approver:
                self.write({'state': 'second_approval', 'first_approval': True})

            if second_approver and not self.first_approval:
                raise ValidationError(_('This order need to first arroval!'))
            if self.first_approval and  (second_approver and not self.second_approval):
                self.write({'second_approval': True})
                approved = True

        if approved or not self.company_id.purchase_approval:
            super(PurchaseOrder, self).button_approve()
            # self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
            # self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            # self._create_picking()
        return {}

    def _create_picking(self):
        if not self.company_id.purchase_approval or (self.company_id.po_double_validation == 'one_step' and self.first_approval) or (self.company_id.po_double_validation == 'two_step' and self.second_approval):
            return super(PurchaseOrder, self)._create_picking()
        return True

    def button_cancel(self):
        for order in self:
            order.write({'first_approval': False, 'second_approval': False})
        return super(PurchaseOrder, self).button_cancel()
