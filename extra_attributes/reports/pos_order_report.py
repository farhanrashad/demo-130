# -*- coding: utf-8 -*-

from functools import partial

from odoo import models, fields


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    product_fabric_id = fields.Many2one('attribute.fabric', string="Fabric")
    product_quality_id = fields.Many2one('product.quality', string="Product Quality")
    product_season_id = fields.Many2one('attribute.season', string="Season")
    product_year_id = fields.Many2one('attribute.year', string="Year")
    launch_date = fields.Date(string="Launch Date")
    product_fit_id = fields.Many2one('attribute.fit', string="Fit")
    fabric_consumption_id = fields.Many2one('fabric.consumption', string="Fabric Composition")
    collection_id = fields.Many2one('attribute.collection', string="Collection")
    style_id = fields.Many2one('attribute.style', string="Style")

    def _select(self):
        return super(PosOrderReport, self)._select() + """
        ,pt.product_fabric_id AS product_fabric_id
        ,pt.product_quality_id AS product_quality_id
        ,pt.product_season_id AS product_season_id
        ,pt.product_year_id AS product_year_id
        ,pt.launch_date AS launch_date
        ,pt.product_fit_id AS product_fit_id
        ,pt.fabric_consumption_id AS fabric_consumption_id
        ,pt.collection_id AS collection_id
        ,pt.style_id AS style_id
        """

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + """
            ,pt.product_fabric_id
            ,pt.product_quality_id
            ,pt.product_season_id
            ,pt.product_year_id
            ,pt.launch_date
            ,pt.product_fit_id
            ,pt.fabric_consumption_id
            ,pt.collection_id
            ,pt.style_id
        """