from odoo import models, fields, api, _

class Picking(models.TransientModel):
    _name = 'picking.picking'
    _description = 'this is picking model'

    picking_ids = fields.Many2one('stock.warehouse.transfer', string='Picking Name')
    picking_date = fields.Date(string='Picking Date', default=fields.Date.today)
    from_warehouse_id_picking = fields.Many2one('stock.warehouse', string='Warehouse From')
    to_warehouse_id_picking = fields.Many2one('stock.warehouse', string='Warehouse To')
    from_location_id_picking = fields.Many2one('stock.warehouse', string='Location From')
    to_location_id_picking = fields.Many2one('stock.warehouse', string='Location To')

    def picking_count(self):
        vals = {
            'picking_id_ship': self.picking_ids.id,
            'picking_creation_date': self.picking_date,
            'wareh_from': self.from_warehouse_id_picking,
            'ware_to': self.to_warehouse_id_picking,
            'from_loc': self.from_location_id_picking,
            'to_loc': self.to_location_id_picking
        }
        self.picking_ids.message_post(body='Picking created successfully', subject='Picking creation')
        self.env['stock.warehouse.transfer'].create(vals)

    # def get_data(self):
    #     print('get data')
    #     course = self.env['stock.warehouse.transfer'].search([('picking_ids_is', '=', self.id)])
    #     print('course', course)
    #     for i in course:
    #         print('courses', i.course_name)
