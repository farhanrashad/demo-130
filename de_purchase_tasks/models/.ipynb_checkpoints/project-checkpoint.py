from odoo import models, fields, api, _


class Project(models.Model):
    _inherit = 'project.project'

    purchase_order_id = fields.Many2one('purchase.order', 'Purchase ID')
    # po_count = fields.Integer('PO Count', compute='_compute_po_count')
    #
    # def _compute_po_count(self):
    #     for rec in self:
    #         self.po_count = self.env['purchase.order'].search_count([('origin', '=', rec.name)])

    
    
class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    purchase_project = fields.Many2one('project.project', string="Project")
    
    note = fields.Char(string='Default Note')
    module_crm = fields.Boolean(string='CRM')
    product_ids = fields.Many2many('product.product', string='Medicines')

#     def set_values(self):
#         res = super(PurchaseConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].set_param('de_purchase_tasks.note', self.note)
#         print("test", self.product_ids.ids)
#         self.env['ir.config_parameter'].set_param('de_purchase_tasks.product_ids', self.product_ids.ids)
#         return res

#     @api.model
#     def get_values(self):
#         res = super(PurchaseConfigSettings, self).get_values()
#         ICPSudo = self.env['ir.config_parameter'].sudo()
#         notes = ICPSudo.get_param('de_purchase_tasks.note')
#         product_ids = self.env['ir.config_parameter'].sudo().get_param('de_purchase_tasks.product_ids')
#         if product_ids:
#             res.update(
#                 note=notes,
#                 product_ids=[(6, 0, literal_eval(product_ids))],
#             )
#         return res
    
    def set_values(self):
        res = super(PurchaseConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('de_purchase_tasks.purchase_project', self.purchase_project)
        return res

    @api.model
    def get_values(self):
        result = super(PurchaseConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        purchase_setting.id = ICPSudo.get_param('de_purchase_tasks.purchase_project')
        result.update(
            purchase_project = purchase_setting
        )
        return result
