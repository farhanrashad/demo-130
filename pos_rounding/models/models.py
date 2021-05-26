# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    allow_rounding = fields.Boolean(string='Allow Automatic Rounding',default=1)
    decimal_rounding = fields.Integer(string='Decimal Rounding', default=1)
    used_for_rounding = fields.Boolean(string='Used For Rounding')
    visible_in_pos = fields.Boolean(string='Visible In Pos', default=1)

    @api.constrains('used_for_rounding')
    def rounding_payment_method_validation(self):
        record = self.search([('used_for_rounding', '=', 'True')])
        if len(record) == 2:
            raise ValidationError("You can create only one rounding payment method.")
        
    @api.constrains('decimal_rounding')
    def decimal_rounding_validation(self):
        if self.used_for_rounding and self.decimal_rounding <=0:
            raise ValidationError("Decimal rounding value must me greater than zero.")
