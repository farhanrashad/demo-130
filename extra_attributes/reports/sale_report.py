# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    product_fabric_id = fields.Many2one('attribute.fabric', string="Fabric")
    product_quality_id = fields.Many2one('product.quality', string="Product Quality")
    product_season_id = fields.Many2one('attribute.season', string="Season")
    product_year_id = fields.Many2one('attribute.year', string="Year")
    launch_date = fields.Date(string="Launch Date")
    product_fit_id = fields.Many2one('attribute.fit', string="Fit")
    fabric_consumption_id = fields.Many2one('fabric.consumption', string="Fabric Composition")
    collection_id = fields.Many2one('attribute.collection', string="Collection")
    style_id = fields.Many2one('attribute.style', string="Style")

    # pylint:disable=dangerous-default-value
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['product_fabric_id'] = ", t.product_fabric_id as product_fabric_id"
        groupby += ', t.product_fabric_id'
        fields['product_quality_id'] = ", t.product_quality_id as product_quality_id"
        groupby += ', t.product_quality_id'
        fields['product_season_id'] = ", t.product_season_id as product_season_id"
        groupby += ', t.product_season_id'
        fields['product_year_id'] = ", t.product_fabric_id as product_year_id"
        groupby += ', t.product_year_id'
        fields['launch_date'] = ", t.launch_date as launch_date"
        groupby += ', t.launch_date'
        fields['product_fit_id'] = ", t.product_fit_id as product_fit_id"
        groupby += ', t.product_fit_id'
        fields['fabric_consumption_id'] = ", t.fabric_consumption_id as fabric_consumption_id"
        groupby += ', t.fabric_consumption_id'
        fields['collection_id'] = ", t.collection_id as collection_id"
        groupby += ', t.collection_id'
        fields['style_id'] = ", t.style_id as style_id"
        groupby += ', t.style_id'
        return super(SaleReport, self)._query(
            with_clause, fields, groupby, from_clause
        )
