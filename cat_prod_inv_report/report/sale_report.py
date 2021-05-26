# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    brand_id = fields.Many2one('brand.brand', string="Brand", readonly=True)
    series_id = fields.Many2one('series.series', string="Series", readonly=True)
    status_id = fields.Many2one('product.status', string="Status", readonly=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', default='male', track_visibility='onchange',help="Your Gender is ", readonly=True)
    liquidation_id = fields.Many2one('product.liquidation', string="Liquidation", readonly=True)
    case_material_id = fields.Many2one('product.case.material', string="Case Material", readonly=True)
    case_shape_id = fields.Many2one('product.case.shape', string="Product Case Shape", readonly=True)
    color_family_id = fields.Many2one('color.family', string="Color Family", readonly=True)
    product_features_id = fields.Many2one('product.features', string="Product Features", readonly=True)
    product_movement_id = fields.Many2one('product.movement', string="Product Movement", readonly=True)
    product_size_id = fields.Many2one('product.size', string="Product Size", readonly=True)
    strap_material_id = fields.Many2one('product.strap.material', string="Strap Material", readonly=True)
    frame_color_id = fields.Many2one('product.frame.color', string="Frame Color", readonly=True)
    frame_shape_id = fields.Many2one('frame.shape', string="Frame Shape", readonly=True)
    lens_color_id = fields.Many2one('lens.color', string="Lens Color", readonly=True)
    lens_features_id = fields.Many2one('lens.features', string="Lens Features", readonly=True)
    frame_material_id = fields.Many2one('frame.material', string="Frame Material", readonly=True)
    partner_shipping_id = fields.Many2one('res.partner', string="Delivery", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['brand_id'] = ", t.brand_id"
        fields['series_id'] = ', t.series_id'
        fields['status_id'] = ", t.status_id"
        fields['gender'] = ', t.gender'

        fields['liquidation_id'] = ", t.liquidation_id"
        fields['case_material_id'] = ', t.case_material_id'

        fields['case_shape_id'] = ", t.case_shape_id"
        fields['color_family_id'] = ', t.color_family_id'

        fields['product_features_id'] = ", t.product_features_id"
        fields['product_movement_id'] = ', t.product_movement_id'

        fields['product_size_id'] = ", t.product_size_id"
        fields['strap_material_id'] = ', t.strap_material_id'

        fields['frame_color_id'] = ", t.frame_color_id"
        fields['frame_shape_id'] = ', t.frame_shape_id'

        fields['lens_color_id'] = ", t.lens_color_id"
        fields['lens_features_id'] = ', t.lens_features_id'

        fields['frame_material_id'] = ", t.frame_material_id"
        fields['partner_shipping_id'] = ', s.partner_shipping_id'


        groupby += ', t.brand_id'
        groupby += ', t.series_id'
        groupby += ', t.status_id'
        groupby += ', t.gender'
        groupby += ', t.liquidation_id'
        groupby += ', t.case_material_id'
        groupby += ', t.case_shape_id'
        groupby += ', t.color_family_id'
        groupby += ', t.product_features_id'
        groupby += ', t.product_movement_id'
        groupby += ', t.product_size_id'
        groupby += ', t.strap_material_id'
        groupby += ', t.frame_color_id'
        groupby += ', t.frame_shape_id'
        groupby += ', t.lens_color_id'
        groupby += ', t.lens_features_id'
        groupby += ', t.frame_material_id'
        groupby += ', s.partner_shipping_id'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

