from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleCommissionMakeInvoice(models.TransientModel):
    _name = "sale.commission.make.invoice"
    _description = "Wizard for making an invoice from a settlement"

    def _default_journal_id(self):
        return self.env["account.journal"].search([("type", "=", "purchase")])[:1]

    def _default_settlement_ids(self):
        return self.env.context.get("settlement_ids", [])

    def _default_from_settlement(self):
        return bool(self.env.context.get("settlement_ids"))

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        required=True,
        domain="[('type', '=', 'purchase')]",
        default=_default_journal_id,
    )
    company_id = fields.Many2one(
        comodel_name="res.company", related="journal_id.company_id", readonly=True
    )
    product_id = fields.Many2one(
        string="Product for invoicing", comodel_name="product.product", required=True
    )
    settlement_ids = fields.Many2many(
        comodel_name="sale.commission.settlement",
        relation="sale_commission_make_invoice_settlement_rel",
        column1="wizard_id",
        column2="settlement_id",
        domain="[('state', '=', 'settled'),('agent_type', '=', 'agent'),"
        "('company_id', '=', company_id)]",
        default=_default_settlement_ids,
    )

    agent_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('agent', '=', True)]",
        ondelete="restrict",
        required=True,
    )

    @api.onchange("agent_id")
    def _compute_settlement_lines(self):
        data = []

        for record in self:
            settlements = self.env['sale.commission.settlement'].search([('agent_id', '=', record.agent_id.id),
                                                                         ("state", "=", "settled")])
            # if not settlements:
            #     for line in self.settlement_ids:
            #         line.unlink()
            flag = False
            if settlements:
                for settlement in settlements:
                    data.append(settlement.id)
            else:
                self.settlement_ids = None
        self.settlement_ids = data

    from_settlement = fields.Boolean(default=_default_from_settlement)
    date = fields.Date(default=fields.Date.context_today)

    def button_create(self):
        self.ensure_one()
        if self.settlement_ids:
            settlements = self.settlement_ids
        else:
            settlements = self.env["sale.commission.settlement"].search(
                [
                    ("state", "=", "settled"),
                    ("agent_type", "=", "agent"),
                    ("company_id", "=", self.journal_id.company_id.id),
                ]
            )
        invoices = settlements.make_invoices(
            self.journal_id, self.product_id, date=self.date
        )
        # go to results
        if len(settlements):
            return {
                "name": _("Created Invoices"),
                "type": "ir.actions.act_window",
                "views": [[False, "list"], [False, "form"]],
                "res_model": "account.move",
                "domain": [["id", "in", invoices.ids]],
            }
