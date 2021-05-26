# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class DailySMS(models.Model):
    _name = "daily.sms"

    name = fields.Char(string='Name', default='Daily SMS Send Action')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='inactive')
    partner_ids = fields.Many2many('res.partner', string='Contacts')

    def sort_by_qty(self, sub_li): 
        l = len(sub_li) 
        for i in range(0, l): 
            for j in range(0, l-i-1): 
                if (sub_li[j][1] > sub_li[j + 1][1]): 
                    tempo = sub_li[j] 
                    sub_li[j]= sub_li[j + 1] 
                    sub_li[j + 1]= tempo 
        return sub_li

    def send_category_sms(self, sorted_data, active_ids):
        sms_text2 = ""
        for name, qty, amount in sorted_data:
            sms_text2 += "%s - %s - %s \n" % (name, int(qty), round(amount, 2))

        for rec in active_ids:
            for partner in rec.partner_ids.filtered(lambda x: x.mobile):
                self.env['telenor.sms'].send({'partner_id': partner.id, 'mobile': partner.mobile, 'message': sms_text2})


    def send_shop_sms(self, shop_ids, order_lines, active_ids):
        shop_data = []
        sms_text3 = ""
        for shop in shop_ids:
            sms3_lines = order_lines.filtered(lambda x: x.order_id.shop_id.id == shop.id)
            shop_data.append([shop.name, sum(sms3_lines.mapped('price_subtotal_incl'))])

        for name, amount in shop_data:
            sms_text3 += "%s - %s\n" % (name, round(amount, 2))

        for rec in active_ids:
            for partner in rec.partner_ids.filtered(lambda x: x.mobile):
                self.env['telenor.sms'].send({'partner_id': partner.id, 'mobile': partner.mobile, 'message': sms_text3})

    def send_sms1(self):
        # SMS 1 : Daily Sales
        order_lines = self.env['pos.order.line'].sudo().search([
            ('create_date', '>=', fields.Date.today().strftime('%Y-%m-%d') + ' 00:00:00'),
            ('create_date', '<=', fields.Date.today().strftime('%Y-%m-%d') + ' 23:59:59'),
            ('order_id.state', 'not in', ('draft', 'cance;'))
        ])
        discounted_sale = sum(order_lines.filtered(lambda x: x.promo_disc_percentage > 0).mapped('price_subtotal_incl'))
        fresh_sale = sum(order_lines.filtered(lambda x: x.promo_disc_percentage == 0).mapped('price_subtotal_incl'))
        total_sale = discounted_sale + fresh_sale
        sms_text = "\nDiscounted Sale - %s \nFresh Sale-Sale Value - %s \nTotal-Sale Value - %s" % (round(discounted_sale, 2), round(fresh_sale, 2), round(total_sale, 2))
        active_ids = self.search([('status', '=', 'active')])
        for rec in active_ids:
            for partner in rec.partner_ids.filtered(lambda x: x.mobile):
                self.env['telenor.sms'].send({'partner_id': partner.id, 'mobile': partner.mobile, 'message': sms_text})

        # # SMS 2 : Category wise Sales
        categ_ids = order_lines.mapped('product_id.categ_id')
        data = []
        for categ in categ_ids:
            lines = order_lines.filtered(lambda x: x.product_id.categ_id.id == categ.id)
            data.append([categ.name, sum(lines.mapped('qty')), sum(lines.mapped('price_subtotal_incl'))])
        
        sorted_data = self.sort_by_qty(data)

        if len(sorted_data) > 20:
            n = 20
            categ_list = [sorted_data[i * n:(i + 1) * n] for i in range((len(sorted_data) + n - 1) // n )]
            for c_list in categ_list:
                self.send_category_sms(c_list, active_ids)
        else:
            self.send_category_sms(sorted_data, active_ids)

        # SMS 3 : Shop wise Sales

        shop_ids = order_lines.mapped('order_id.shop_id')
        sms_text3 = ""
        if len(shop_ids) > 20:
            n = 20
            my_list = shop_ids.ids
            shop_list = [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]
            for s_list in shop_list:
                self.send_shop_sms(self.env['pos.multi.shop'].browse(s_list), order_lines, active_ids)
        else:
            self.send_shop_sms(shop_ids, order_lines, active_ids)
