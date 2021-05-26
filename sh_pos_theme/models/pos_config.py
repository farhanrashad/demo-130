from odoo import api, fields, models, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    button_layout = fields.Boolean(compute="_compute_button_layout")

    def _compute_button_layout(self):
        params = self.env['ir.config_parameter'].sudo()
        col = params.get_param('pos_button_col', default='False')
        pos = params.get_param('pos_button_position', default='False')
        self.button_layout = (col == 'default' and pos == 'default')
