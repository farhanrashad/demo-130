from odoo import models, fields, api, _


class Project(models.Model):
    _inherit = 'project.project'

    purchase_order_id = fields.Many2one('purchase.order', 'Purchase ID')
    # po_count = fields.Integer('PO Count', compute='_compute_po_count')
    #
    # def _compute_po_count(self):
    #     for rec in self:
    #         self.po_count = self.env['purchase.order'].search_count([('origin', '=', rec.name)])
