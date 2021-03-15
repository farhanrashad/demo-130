from odoo import api, fields, models
from odoo.exceptions import UserError


class Producttemplate(models.Model):
    _inherit = 'product.template'

    sale_price_comp = fields.Selection([('cost price', 'Cost Price'), ('vendor total cost', 'Vendor Total Cost')],
                                       default='vendor total cost', required=True, string='Sale Price Computation')
    percentage_addition = fields.Float(string='Percentage addition')
    min_profit = fields.Float(string='Minimum Profit')
    min_sale = fields.Float(string='Minimum Sale', readonly=True)

    @api.constrains('min_sale', 'min_profit', 'percentage_addition')
    def compute_min_amount(self):
        # if self.min_sale > 100 or self.min_sale < 0:
        #     raise UserError("**Minimum Sale percent** cannot be greater than 100")
        if self.min_profit > 100 or self.min_profit < 0:
            raise UserError("**Minimum Profit percent** cannot be greater than 100")
        if self.percentage_addition > 100 or self.percentage_addition < 0:
            raise UserError("**Addition percent** cannot be greater than 100")
        # if not self.seller_ids:
        #     raise UserError("No vendor exits")

    def cost_cal(self):
        flag = 0
        if self.sale_price_comp == 'vendor total cost':
            if self.percentage_addition >= 0:
                if self.seller_ids:
                    for vendor in self.seller_ids:
                        if vendor.is_applicable == True:
                            flag = 1
                            total = vendor.total_cost + ((vendor.total_cost / 100) * self.percentage_addition)
                            currency = self.env['res.currency'].search([('active','=',True),('id','=',vendor.currency_id.id)])
                            total = total * currency.rate
                            self.list_price = total
                            break
                        else:
                            continue
                    if flag == 0:
                        self.list_price = 0

        if self.sale_price_comp == 'cost price':
            if self.percentage_addition >= 0:
                for purchase in self:
                    total = purchase.standard_price + ((purchase.standard_price / 100) * self.percentage_addition)

                    currency = self.env['res.currency'].search([('active','=',True),('name','=',vendor.currency_id.id)])
                    total = total * currency.rate
                    self.list_price = total
                    break

    @api.onchange('seller_ids')
    def onchange_seller_ids(self):
        self.cost_cal()

    @api.onchange('percentage_addition', 'sale_price_comp')
    def onchange_sale_price(self):
        self.cost_cal()

    @api.onchange('min_sale', 'min_profit', 'list_price')
    def onchange_profit_sale_price(self):
        for rec in self:
            if rec.percentage_addition > 0:
                total_profit = rec.list_price - ((rec.list_price / 100) * rec.min_profit)
                rec.min_sale = total_profit


class ProductVendorPrice(models.Model):
    _inherit = 'product.supplierinfo'

    is_applicable = fields.Boolean(string="Applicable")
    est_landed_cost = fields.Float(string="Estimated Landed Cost %")
    total_cost = fields.Float(string="Total Cost", compute='_compute_amount')

    @api.depends('price', 'est_landed_cost')
    def _compute_amount(self):
        for line in self:
            total = line.price + ((line.price / 100) * line.est_landed_cost)
            line.total_cost = total


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # @api.constrains('price_unit')
    # def constraint_price_unit(self):
    #     print(self)
    #     # if self.price_unit < self.product_id.min_sale:
    #     #     raise UserError("Unit price cannot be less than Product Sale Amount")
    #
