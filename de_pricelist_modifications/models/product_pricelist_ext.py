# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductPriceListExt(models.Model):
    _inherit = 'product.pricelist'

    def write(self, vals):
        old_line = []
        new_lines = []
        result = []
        old_records = self.env['product.pricelist.item'].search([('pricelist_id', '=', self.id)])
        for old in old_records:
            old_line.append(old.id)
        res = super(ProductPriceListExt, self).write(vals)
        new_records = self.env['product.pricelist.item'].search([('pricelist_id', '=', self.id)])
        for new in new_records:
            new_lines.append(new.id)
        set1 = set(old_line)
        set2 = set(new_lines)
        set3 = set2 - set1
        result = list(set3)
        list1 = []
        new_id = []
        for ref in self.ref_price_list_ids.ids:
            list1.append(ref)
        items = self.env['product.pricelist'].search([('id', 'in', list1)])
        new_added = self.env['product.pricelist.item'].search([('id', 'in', result)])
        for item in items:
            for line in new_added:
                item_line = {
                    'pricelist_id': item.id,
                    'applied_on': line.applied_on,
                    'product_tmpl_id': line.product_tmpl_id.id,
                    'compute_price': line.compute_price,
                    'fixed_price': line.fixed_price,
                    'min_quantity': line.min_quantity,
                }
                created = item.item_ids.create(item_line)
        return res

    ref_price_list_ids = fields.Many2many(comodel_name='product.pricelist', string='Ref PriceList',
                                          relation='product_price_rel', column1='m2m_id', column2='assets_id')
