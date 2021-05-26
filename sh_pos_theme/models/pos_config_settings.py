# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_config_theme = fields.Selection([('defaulttheme', 'Default Theme'), ('sh pos theme assets blue', 'Blue Theme'), ('sh pos theme assets green', 'Green Theme'), ('sh pos theme assets red', 'Red Theme'), ('sh pos theme assets org', 'Orange Theme'), ('sh pos theme assets teal', 'Teal Theme'), ('sh pos theme assets cyan', 'Cyan Theme'), ('sh pos theme assets indigo', 'Indigo Theme')], string="POS Theme")
    pos_button_col = fields.Selection([
        ('default', 'Default'),
        ('numpad_col_1', '1'),
        ('numpad_col_2', '2'),
        ('numpad_col_3', '3'),
    ], string="No of Column")
    pos_button_position = fields.Selection([
        ('default', 'Default'),
        ('_left', 'Left of the cart'),
        ('_right', 'Right of the cart'),
    ], string="Button Position")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        params.get_param('pos_config_theme', default='False')
        params.get_param('pos_button_col', default='False')
        params.get_param('pos_button_position', default='False')
        res.update(
            pos_config_theme=params.get_param('pos_config_theme', default='defaulttheme'),
            pos_button_col=params.get_param('pos_button_col', default='default'),
            pos_button_position=params.get_param('pos_button_position', default='default'),
        )
        return res
 
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("pos_config_theme", self.pos_config_theme or "")
        self.env['ir.config_parameter'].sudo().set_param("pos_button_col", self.pos_button_col or "")
        self.env['ir.config_parameter'].sudo().set_param("pos_button_position", self.pos_button_position or "")
        view_ids = self.env['ir.ui.view'].search([('name', 'in', ('sh pos theme assets green', 'sh pos theme assets blue', 'sh pos theme assets cyan', 'sh pos theme assets red', 'sh pos theme assets indigo', 'sh pos theme assets org', 'sh pos theme assets teal'))])
        if view_ids: 
            for rec in view_ids:                
                if rec.name == self.pos_config_theme:
                    rec.write({'active':True})
                else:
                    rec.write({'active':False})                       
        view_list = [
            'numpad_col_1_left',
            'numpad_col_2_left',
            'numpad_col_3_left',
            'numpad_col_1_right',
            'numpad_col_2_right',
            'numpad_col_3_right',
        ]
        button_asset_ids = self.env['ir.ui.view'].search([('name', 'in', view_list)])
        for rec in button_asset_ids:
            if rec.name == self.pos_button_col+self.pos_button_position:
                rec.write({'active': True})
            else:
                rec.write({'active': False})
