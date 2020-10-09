from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccMoveInh(models.Model):
    _inherit = 'account.move'
    _name = 'account.move'

    # reference = fields.Integer('Reference')

    @api.model
    def create(self, vals):

        ref_field = vals['ref']

        sql = """ select ref from account_move where ref ='""" + str(ref_field) + """' """
        self.env.cr.execute(sql)
        exists = self.env.cr.fetchone()

        contains_digit = ref_field.isdigit()
        if not contains_digit:
            raise UserError(('Sorry! Only Integer Values are allowed in Reference field.'))

        if exists:
            raise UserError(('A Reference already exists.'))
        else:
            pass

        result = super(AccMoveInh, self).create(vals)
        return result
