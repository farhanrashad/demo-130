# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError, ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    department_restrict_id = fields.Many2one('purchase.department', 'Department', states=READONLY_STATES)
    is_alert = fields.Boolean(compute='_compute_is_alert')

    def _compute_is_alert(self):
        for po in self:
            if not self.env.user.department_ids and self.env.user.has_group('purchase_department_restrictions.group_restrict_department'):
                po.is_alert = True
            else:
                po.is_alert = False

    @api.model
    def default_get(self, fields):
        vals = super(PurchaseOrder, self).default_get(fields)
        department_restrict_id = self.env.user.department_ids.filtered(lambda x: x.is_default)
        if department_restrict_id:
            vals['department_restrict_id'] = department_restrict_id.department_id.id
        if not self.env.user.department_ids and self.env.user.has_group('purchase_department_restrictions.group_restrict_department'):
            vals['is_alert'] = True
        return vals

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    department_restrict_id = fields.Many2one('purchase.department', 'Department')


class Department(models.Model):
    _name = 'purchase.department'

    name = fields.Char('Department', required=True)
    is_default = fields.Boolean('Is Default')


class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_department = fields.Boolean('Restrict by Department')
    temp_department_ids = fields.Many2many(
        'purchase.department',
        'department_security_purchase_users',
        'user_id',
        'department_id',
        'Departments')
    department_ids = fields.One2many(
        'user.department',
        'user_id',
        'Departments')

    department_count = fields.Integer(compute='_compute_department_count')

    @api.model
    def create(self, values):
        self.env['user.department'].clear_caches()
        return super(ResUsers, self).create(values)

    def write(self, values):
        self.env['user.department'].clear_caches()
        return super(ResUsers, self).write(values)

    @api.constrains('department_ids')
    def _check_department_ids(self):
        if len(self.department_ids.filtered(lambda x: x.is_default)) > 1:
            raise ValidationError(_('You cannot set more then one department as default'))
    
    @api.depends('department_ids')
    def _compute_department_count(self):
        for user in self:
            user.department_count = len(user.department_ids)
            user.temp_department_ids = [(6, 0, [dep.department_id.id for dep in user.department_ids])]

class UserDepartment(models.Model):
    _name = 'user.department'

    user_id = fields.Many2one('res.users')
    department_id = fields.Many2one('purchase.department', required=True)
    is_default = fields.Boolean('Is Default')
