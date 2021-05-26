# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    brand_id = fields.Many2one(string="Brand", comodel_name='brand.brand' , readonly=True,)
    series_id = fields.Many2one('series.series', string="Series", readonly=True,)
    status_id = fields.Many2one('product.status', string="Status")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', default='male',help="Your Gender is ")
    liquidation_id = fields.Many2one('product.liquidation', string="Liquidation")
    case_material_id = fields.Many2one('product.case.material', string="Case Material")
    case_shape_id = fields.Many2one('product.case.shape', string="Product Case Shape")
    color_family_id = fields.Many2one('color.family', string="Color Family")
    product_features_id = fields.Many2one('product.features', string="Product Features")
    product_movement_id = fields.Many2one('product.movement', string="Product Movement")
    product_size_id = fields.Many2one('product.size', string="Product Size")
    strap_material_id = fields.Many2one('product.strap.material', string="Strap Material")
    frame_color_id = fields.Many2one('product.frame.color', string="Frame Color")
    frame_shape_id = fields.Many2one('frame.shape', string="Frame Shape")
    lens_color_id = fields.Many2one('lens.color', string="Lens Color")
    lens_features_id = fields.Many2one('lens.features', string="Lens Features")
    frame_material_id = fields.Many2one('frame.material', string="Frame Material")

    def _select(self):
        return super(PurchaseReport, self)._select() + ",t.brand_id, t.gender, t.status_id, t.series_id, t.liquidation_id, t.case_material_id, t.case_shape_id, t.color_family_id, t.product_features_id, t.product_movement_id, t.product_size_id, t.strap_material_id, t.frame_color_id, t.frame_shape_id, t.lens_color_id, t.lens_features_id, t.frame_material_id"


    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + ",t.brand_id, t.gender, t.status_id, t.series_id, t.liquidation_id, t.case_material_id, t.case_shape_id, t.color_family_id, t.product_features_id, t.product_movement_id, t.product_size_id, t.strap_material_id, t.frame_color_id, t.frame_shape_id, t.lens_color_id, t.lens_features_id, t.frame_material_id"
