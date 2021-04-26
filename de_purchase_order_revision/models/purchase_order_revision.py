from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    prev_order_seq = fields.Boolean('Invoice seq', default=False)
    is_order_revision = fields.Boolean('Revision', default=False)
    purchase_order_revision = fields.Char('Purchase Order Revision')
    order_revisions_count = fields.Integer(string='Order Revisions', compute='_compute_order_revisions_count')
    current_order_revision_id = fields.Many2one('purchase.order', string='Current Order Revision', readonly=True,
                                                copy=True)
    old_order_revision_ids = fields.One2many('purchase.order', 'current_order_revision_id',
                                             string='Old Order Revisions',
                                             readonly=True,
                                             context={'active_test': False})
    order_revision_number = fields.Integer('Revision', copy=True)
    unrevisioned_order_name = fields.Char('Order Reference', copy=False, readonly=True)

    # invoice_count = fields.Char('invoice')
    # invoice_ids = fields.Char('invoice ids')

    @api.depends('old_order_revision_ids')
    def _compute_order_revisions_count(self):
        count = 0
        for rec in self:
            if rec.old_order_revision_ids:
                for line in rec.old_order_revision_ids:
                    count = count + 1
                rec.order_revisions_count = count
            else:
                rec.order_revisions_count = count

    def order_view_revision(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Revision'),
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('current_order_revision_id', '=', self.id)],
            'context': dict(self._context, create=False, default_current_order_revision_id=self.id),
        }

    @api.model
    def create(self, vals):
        count = 1
        if 'is_order_revision' in vals:
            if vals.get('is_order_revision') == True:
                seq = vals.get('prev_order_seq')
                pri = self.search([('name', '=', seq)])
                for line in pri.old_order_revision_ids:
                    count = count + 1
                vals['name'] = seq + '-' + str(count)
        return super(PurchaseOrder, self).create(vals)

    def action_order_revision(self):
        self.ensure_one()
        purchase_order = self.env['purchase.order'].create({
            'prev_order_seq': self.name,
            'is_order_revision': True,
            'state': 'draft',
            'partner_id': self.partner_id.id,
            # 'partner_ref': self.partner_ref,
            'date_order': self.date_order,
            # 'date_planned': self.date_planned,
            'current_order_revision_id': self.id,
        })

        if self.order_line:
            for line in self.order_line:
                purchase_order_line = self.env['purchase.order.line'].create({
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_qty': line.product_qty,
                    'price_unit': line.price_unit,
                    'taxes_id': line.taxes_id,
                    'price_subtotal': line.price_subtotal,
                    'order_id': purchase_order.id,
                })
