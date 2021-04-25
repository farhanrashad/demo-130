from odoo import api, fields, models, _


class PurchaseDemand(models.Model):
    _inherit = "purchase.demand"

    prev_req_seq = fields.Boolean('Invoice seq', default=False)
    is_requisition_revision = fields.Boolean('Revision', default=False)
    purchase_req_revision = fields.Char('Purchase Requisition Revision')
    req_revisions_count = fields.Integer(string='Requisition Revisions', compute='_compute_req_revisions_count')
    current_req_revision_id = fields.Many2one('purchase.demand', string='Current Requisition Revision', readonly=True,
                                              copy=True)
    old_req_revision_ids = fields.One2many('purchase.demand', 'current_req_revision_id', string='Old Req Revisions',
                                           readonly=True,
                                           context={'active_test': False})
    req_revision_number = fields.Integer('Revision', copy=True)
    unrevisioned_req_name = fields.Char('Order Reference', copy=False, readonly=True)

    invoice_count = fields.Char('invoice')
    invoice_ids = fields.Char('invoice ids')

    @api.depends('old_req_revision_ids')
    def _compute_req_revisions_count(self):
        count = 0
        for rec in self:
            if rec.old_req_revision_ids:
                for line in rec.old_req_revision_ids:
                    count = count + 1
                rec.req_revisions_count = count
            else:
                rec.req_revisions_count = count

    def req_view_revision(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Revision'),
            'res_model': 'purchase.demand',
            'view_mode': 'tree,form',
            'domain': [('current_req_revision_id', '=', self.id)],
            'context': dict(self._context, create=False, default_current_req_revision_id=self.id),
        }

    @api.model
    def create(self, vals):
        count = 0
        if 'is_requisition_revision' in vals:
            if vals.get('is_requisition_revision') == True:
                seq = vals.get('prev_req_seq')
                pri = self.search([('name', '=', seq)])
                for line in pri.old_req_revision_ids:
                    count = count + 1
                vals['name'] = seq + '-' + str(count)
        return super(PurchaseDemand, self).create(vals)

    def action_req_revision(self):
        self.ensure_one()
        purchase_demand = self.env['purchase.demand'].create({
            'prev_req_seq': self.name,
            'is_requisition_revision': True,
            'state': 'draft',
            'user_id': self.user_id.id,
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'demand_type_id': self.demand_type_id.id,
            # 'date_requisition': self.date_requisition,
            'schedule_date': self.schedule_date,
            'current_req_revision_id': self.id,
        })

        if self.purchase_demand_line:
            for line in self.purchase_demand_line:
                purchase_demand_line = self.env['purchase.demand.line'].create({
                    'demand_action': line.demand_action,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom_qty': line.product_uom_qty,
                    'ordered_qty': line.ordered_qty,
                    'product_uom': line.product_uom.id,
                    'schedule_date': line.schedule_date,
                    'partner_id': line.partner_id.id,
                    'purchase_demand_id': purchase_demand.id,
                })
