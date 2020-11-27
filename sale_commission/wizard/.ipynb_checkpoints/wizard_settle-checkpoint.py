# Copyright 2014-2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, fields, models


class SaleCommissionMakeSettle(models.TransientModel):
    _name = "sale.commission.make.settle"
    _description = "Wizard for settling commissions in invoices"

    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date to", required=True)
    agent_ids = fields.Many2many(
        comodel_name="res.partner", domain="[('agent', '=', True)]"
    )

    def _get_period_start(self, agent, date_to):
        if agent.settlement == "monthly":
            return date(month=date_to.month, year=date_to.year, day=1)
        elif agent.settlement == "quaterly":
            # Get first month of the date quarter
            month = (date_to.month - 1) // 3 * 3 + 1
            return date(month=month, year=date_to.year, day=1)
        elif agent.settlement == "semi":
            if date_to.month > 6:
                return date(month=7, year=date_to.year, day=1)
            else:
                return date(month=1, year=date_to.year, day=1)
        elif agent.settlement == "annual":
            return date(month=1, year=date_to.year, day=1)

    def _get_next_period_date(self, agent, current_date):
        if agent.settlement == "monthly":
            return current_date + relativedelta(months=1)
        elif agent.settlement == "quaterly":
            return current_date + relativedelta(months=3)
        elif agent.settlement == "semi":
            return current_date + relativedelta(months=6)
        elif agent.settlement == "annual":
            return current_date + relativedelta(years=1)

    def _get_settlement(self, agent, company, sett_from, sett_to):
        return self.env["sale.commission.settlement"].search(
            [
                ("agent_id", "=", agent.id),
                ("date_from", "=", sett_from),
                ("date_to", "=", sett_to),
                ("company_id", "=", company.id),
                ("state", "=", "settled"),
            ],
            limit=1,
        )

    def _prepare_settlement_vals(self, agent, company, sett_from, sett_to):
        return {
            "agent_id": agent.id,
            "date_from": sett_from,
            "date_to": sett_to,
            "company_id": company.id,
        }

    def action_settle(self):
        # sale_agents = self.env['sale.order'].search([('state','=','sale'),('agent_id','=',self.agent_ids)])
        for record in self:
            # sale_agents = self.env['sale.order'].search([('state', '=', 'sale'), ('agent_id', 'in', record.agent_ids.ids)])
            for agent in record.agent_ids:
                commission = 0
                sale_records = self.env['sale.order'].search([('state', '=', 'sale'),('agent_id','=', agent.id)])
                # sql = """select id from sale_order where state='sale' and agent_id = '""" + str(agent.id) + """'and date(date_order) >='""" + str(record.date_from) + """' and date(date_order) <='""" + str(record.date_to) + """'"""
                # self.env.cr.execute(sql)
                # exists = self.env.cr.fetchone()
                # print(exists)
                if sale_records:
                        for rec in sale_records:
                            if rec.date_order.date() >= record.date_from and rec.date_order.date() <= record.date_to:
                                commission = commission + rec.commission_total
                        self.env['sale.commission.settlement'].create({
                            'agent_id': agent.id,
                            'date_from': record.date_from,
                            'date_to': record.date_to,
                            'total': commission,
                                })