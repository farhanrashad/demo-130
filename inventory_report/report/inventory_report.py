# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools

class StockLocationReport(models.Model):
    _name = "report.stock.location"
    _auto = False
    _description = "Report Stock Location"

    product_id = fields.Many2one('product.product', 'Variant', readonly=True)
    on_hand_qty = fields.Float('On Hand', readonly=True)
    purchase_qty = fields.Float('Purchase', readonly=True)
    incoming_qty = fields.Float('In-transit', readonly=True)
    outgoing_qty = fields.Float('Sale', readonly=True)
    forecast_qty = fields.Float('Forecasted', readonly=True)
    location_id = fields.Many2one('stock.location', 'Location', readonly=True)
    category_id = fields.Many2one('product.category', 'Category', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    create_date = fields.Datetime('Create Date')
    write_date = fields.Datetime('Update Date')
    create_uid = fields.Many2one('res.users', 'Created By')
    write_uid = fields.Many2one('res.users', 'Updated By')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_location')
        query = """
        CREATE or REPLACE VIEW report_stock_location AS (
            SELECT 
                min(sm.id) as id,
                sm.create_date as create_date,
                sm.create_uid as create_uid,
                sm.write_date as write_date,
                sm.write_uid as write_uid,
                p.id as product_id,
                t.categ_id as category_id,
                t.id as product_tmpl_id,
                sl.id as location_id,
                CASE WHEN pt.code = 'outgoing' and sm.sale_line_id is not null and sm.location_id = sl.id and sm.state not in ('done', 'cancel') THEN
                    sum(sm.product_qty) END as outgoing_qty,
                CASE WHEN pt.code = 'incoming' and  sm.location_id = sl.transit_loc and sm.location_dest_id = sl.id and sm.state not in ('done', 'cancel') THEN
                    sum(sm.product_qty) END as incoming_qty,
                CASE WHEN pt.code = 'incoming' and sm.purchase_line_id is not null and sm.location_dest_id = sl.id and sm.state not in ('done', 'cancel') THEN
                    sum(sm.product_qty) END as purchase_qty,
                CASE WHEN sm.location_id = sl.id and sm.state = 'done' THEN
                        -sum(sm.product_qty)
                    WHEN sm.location_dest_id = sl.id and sm.state = 'done'  THEN
                        sum(sm.product_qty)
                    ELSE 0.0
                END AS on_hand_qty,
                CASE WHEN sm.location_id = sl.id and sm.state = 'done' THEN
                        -sum(sm.product_qty)
                    WHEN sm.location_dest_id = sl.id and sm.state = 'done'  THEN
                        sum(sm.product_qty)
                    WHEN pt.code = 'incoming' and  sm.location_id = sl.transit_loc and sm.location_dest_id = sl.id and sm.state not in ('done', 'cancel') THEN
                        sum(sm.product_qty) 
                    ELSE 0.0
                END AS forecast_qty
            FROM stock_location as sl
            LEFT JOIN stock_move as sm on (sm.location_id = sl.id OR sm.location_dest_id = sl.id )
            LEFT JOIN stock_picking_type as pt on (sm.picking_type_id = pt.id)
            LEFT JOIN product_product as p on (p.id = sm.product_id)
            LEFT JOIN product_template t on (p.product_tmpl_id=t.id)
            WHERE sl.usage = 'internal'
            GROUP BY sm.write_uid, sm.create_uid, sm.write_date, sm.create_date, p.id, sm.location_id, sm.location_dest_id, pt.code, sm.state, sl.id, t.categ_id, sm.sale_line_id, t.id, sm.purchase_line_id
        );
        """
        res = self.env.cr.execute(query)