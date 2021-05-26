# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class AccountAccount(models.Model):
    _inherit = 'account.account'

    analytic_type = fields.Selection([
        ('gross_sale', 'Gross Sale'),
    	('cogs', 'COGS'),
    	('admin_expense', 'Admin Expenses'),
    	('selling_expense', 'Selling Expenses'),
    	('financila_expense', 'Financial Expenses'),
    	('wh_allocation', 'WH Allocation'),
    	('ho_allocation', 'HO Allocation'),
    	('incentive', 'Incentive Sales')
	], string='Analytic Type', copy=False)
