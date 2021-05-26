# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models, api, _


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_fabric_id = fields.Many2one('attribute.fabric', string="Fabric")
    product_quality_id = fields.Many2one('product.quality', string="Product Quality")
    product_season_id = fields.Many2one('attribute.season', string="Season")
    product_year_id = fields.Many2one('attribute.year', string="Year")
    launch_date = fields.Date(string="Launch Date")
    
    @api.model
    def _select(self):
        select_str = super()._select()
        select_str += """
            , template.product_fabric_id as product_fabric_id
            , template.product_quality_id as product_quality_id
            , template.product_season_id as product_season_id
            , template.product_year_id as product_year_id
            , template.launch_date as launch_date
            """
        return select_str
    
    @api.model
    def _from(self):
        from_str = super()._from()
        return from_str
     
    @api.model
    def _where(self):
        where_str = super()._where()
        return where_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", template.product_fabric_id,template.product_quality_id,template.product_season_id,template.product_year_id,template.launch_date"
        return group_by_str
