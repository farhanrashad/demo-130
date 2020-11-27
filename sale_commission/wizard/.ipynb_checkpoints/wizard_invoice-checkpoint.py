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
        string="Product for invoicing", comodel_name="product.product"
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
    
    chart_id = fields.Many2one('account.account',
        required=True)

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
        for record in self:
            if record.settlement_ids:
                total_commission = 0
                for settlement in record.settlement_ids:
                    total_commission = total_commission + settlement.total
                    settlement.state = "invoiced"

                inv_obj = {
                    'partner_id': settlement.agent_id.id,
                    'journal_id': record.journal_id.id,
                    'invoice_date': fields.Date.today(),
                    'type': 'in_invoice',
                    'name': '/',
                    'state': 'draft',
                    'invoice_line_ids': [(0, 0, {'name': 'Comm: '+ settlement.agent_id.name,
                                                 'account_id': record.chart_id.id,
                                                 'quantity': 1.0,
                                                 'price_unit': total_commission, })],
                    }
                    
                record_created = self.env['account.move'].create(inv_obj)
                settlement.account_invoice_id = record_created.id