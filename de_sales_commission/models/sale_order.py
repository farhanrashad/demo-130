# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, Warning

from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one('res.partner', string='Agent Name', required=False, readonly=True,
                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                               help="To address a contact in care of someone else")

    commission_amount = fields.Monetary(string='Commission Amount', readonly=True, store=True,
                                        compute='_amount_commission')  #

    def test_commission(self):
        commission = self.env['sale.commission'].create({
            'name': self.id,
            'agent_id': self.partner_id.id,
            # 'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            # 'product_id': self.product_id.id,
            'commission_amount': self.commission_amount,
            # 'currency_id': self.id,
            'doc_date': self.date_order,
            'sale_id': self.id,
            'sale_amount': self.amount_total,
        })
        commission.action_confirm()


    # ==================================================================
    # here below we can create sale commission from sale order so
    # data get from sale order and auto crate sale commission
    # so we override action_confirm if user click on confirm button indraft field
    #===================================================================
    def action_confirm(self):
        commission = self.env['sale.commission'].create({
            'name': self.id,
            'agent_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            # 'product_id': self.product_id.id,
            'commission_amount': self.commission_amount,
            'doc_date': self.date_order,
            'sale_id': self.id,
            'sale_amount': self.amount_total,
        })
        commission.action_confirm()
        res = super(SaleOrder, self).action_confirm()

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()

    # =================================================================
    # this code below will automatically set comm. % in order_line in as we change customer
    # =================================================================
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.agent_id = self.partner_id.agent_id or False
        self.commission_percentage = self.partner_id.commission_percent

    # ====================================================================
    # order_line.price_subtotal   also added in depends
    # i remove order_id and change commission_percentage to commission_percent
    # ====================================================================
    @api.depends('order_line.commission_percentage')  # ,'order_line.price_subtotal'
    def _amount_commission(self):
        """Compute the Commission amounts of the SO"""
        total = 0
        res = super(SaleOrder, self)._amount_all()
        if self.partner_id.commission_percent:
            for line in self.order_line:
                total += (line.commission_percentage / 100) * line.price_subtotal

            self.commission_amount = total

        return res

    @api.depends('order_line.price_total')
    def _amount_all_com(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
                'commission_amount': self.commission_amount,
            })

    def recompute_lines_agents(self):
        if self.order_id.partner_id.commission_percent:
            for line in self.order_line:
                line.update({
                    'commission_percentage': self.partner_id.commission_percentage
                })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    commission_percentage = fields.Float(string='Comm. %', readonly=True,
                                         states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
                                         )

    @api.onchange('product_id')
    def onchange_product_id(self):
        # super(SaleOrderLine, self).onchange_product_id()
        if self.order_id.partner_id.commission_percent:
            self.commission_percentage = self.order_id.partner_id.commission_percent
