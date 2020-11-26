# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    agent_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('agent', '=', True)]",
        ondelete="restrict",
        required=True,
    )

    @api.onchange("amount_total")
    def _compute_commission(self):
        for record in self:
            flag = False
            if record.agent_id.commission_id.commission_type == 'section':
                rules = self.env['sale.commission'].search([('id', '=', record.agent_id.commission_id.id)])
                print('success!')
                for rule in rules.section_ids:
                    if self.amount_total > rule.amount_from and self.amount_total < rule.amount_to:
                        flag = True
                        commission = (rule.percent * self.amount_total) / 100
                        self.commission_total = commission
                if not flag:
                    raise UserError(('No Rate definition found for this amount total, against applied agent: ' + record.agent_id.name ))



    @api.depends("order_line.agent_ids.amount")
    def _compute_commission_total(self):
        for record in self:
            record.commission_total = sum(record.mapped("order_line.agent_ids.amount"))

    commission_total = fields.Float(
        string="Commissions", compute="_compute_commission_total", store=True,
    )

    def recompute_lines_agents(self):
        self.mapped("order_line").recompute_agents()


class SaleOrderLine(models.Model):
    _inherit = [
        "sale.order.line",
        "sale.commission.mixin",
    ]
    _name = "sale.order.line"

    agent_ids = fields.One2many(comodel_name="sale.order.line.agent")

    @api.depends("order_id.partner_id")
    def _compute_agent_ids(self):
        self.agent_ids = False  # for resetting previous agents
        for record in self.filtered(lambda x: x.order_id.partner_id):
            if not record.commission_free:
                record.agent_ids = record._prepare_agents_vals_partner(
                    record.order_id.partner_id
                )

    def _prepare_invoice_line(self):
        vals = super()._prepare_invoice_line()
        vals["agent_ids"] = [
            (0, 0, {"agent_id": x.agent_id.id, "commission_id": x.commission_id.id})
            for x in self.agent_ids
        ]
        return vals


class SaleOrderLineAgent(models.Model):
    _inherit = "sale.commission.line.mixin"
    _name = "sale.order.line.agent"
    _description = "Agent detail of commission line in order lines"

    object_id = fields.Many2one(comodel_name="sale.order.line")
    currency_id = fields.Many2one(related="object_id.currency_id")

    @api.depends(
        "object_id.price_subtotal", "object_id.product_id", "object_id.product_uom_qty"
    )
    def _compute_amount(self):
        for line in self:
            order_line = line.object_id
            line.amount = line._get_commission_amount(
                line.commission_id,
                order_line.price_subtotal,
                order_line.product_id,
                order_line.product_uom_qty,
            )
