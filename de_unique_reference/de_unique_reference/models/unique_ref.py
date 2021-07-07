from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccMoveInh(models.Model):
    _inherit = 'account.move'
    _name = 'account.move'


    @api.model
    def create(self, vals):

        ref_field = vals['ref']
        if ref_field:
            sql = """ select ref from account_move where ref ='""" + str(ref_field) + """' """
            self.env.cr.execute(sql)
            exists = self.env.cr.fetchone()

            if exists:
                raise UserError(('A Reference already exists.'))
            else:
                pass
        else:
            pass

        result = super(AccMoveInh, self).create(vals)
        return result