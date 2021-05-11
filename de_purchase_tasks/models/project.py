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
    
    @api.model
    def get_values(self):
        res = super(PurchaseConfigSettings, self).get_values()

        params = self.env['ir.config_parameter'].sudo()
        purchase_project = params.get_param('purchase_project', default=False)
        res.update(
            purchase_project=int(purchase_project),
        )
        return res

    def set_values(self):
        super(PurchaseConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("purchase_project", self.purchase_project.id)

    
#     def set_values(self):
#         res = super(PurchaseConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].set_param('de_purchase_tasks.purchase_project', self.purchase_project)
#         return res

#     @api.model
#     def get_values(self):
#         result = super(PurchaseConfigSettings, self).get_values()
#         ICPSudo = self.env['ir.config_parameter'].sudo()
#         purchase_setting = ICPSudo.get_param('de_purchase_tasks.purchase_project')
#         result.update(
#             purchase_project = purchase_setting
#         )
#         return result
