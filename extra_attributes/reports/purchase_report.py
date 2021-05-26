# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#
# Please note that these reports are not multi-currency !!!
#

from odoo import api, fields, models, tools


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

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
        return super(PurchaseReport, self)._select() + """
        ,t.product_fabric_id AS product_fabric_id
        ,t.product_quality_id AS product_quality_id
        ,t.product_season_id AS product_season_id
        ,t.product_year_id AS product_year_id
        ,t.launch_date AS launch_date
        ,t.product_fit_id AS product_fit_id
        ,t.fabric_consumption_id AS fabric_consumption_id
        ,t.collection_id AS collection_id
        ,t.style_id AS style_id
        """

    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + """
            ,t.product_fabric_id
            ,t.product_quality_id
            ,t.product_season_id
            ,t.product_year_id
            ,t.launch_date
            ,t.product_fit_id
            ,t.fabric_consumption_id
            ,t.collection_id
            ,t.style_id
        """
